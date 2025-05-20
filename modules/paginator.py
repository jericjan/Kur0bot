# stolen from https://github.com/ErrorNoInternet/disnake-paginator
# button design from pycord lol
# slightly modified
# i should really make this a cog (soon)

from typing import Any, TYPE_CHECKING, Callable, Optional

import disnake

if TYPE_CHECKING:
    from disnake.ext import commands

async def dummy_response(interaction: disnake.ApplicationCommandInteraction[Any]):
    await interaction.response.send_message(
        "You are not the sender of that command!", ephemeral=True
    )


class ChannelResponseWrapper:
    def __init__(self, channel: disnake.abc.Messageable):
        self.channel = channel
        self.sent_message = None

    async def defer(self, ephemeral: Optional[bool] = False):
        self.sent_message = await self.channel.send("I am thinking...")

    async def send_message(self, content: Optional[str] = None, embed: Optional[disnake.embeds.Embed] = None, view: Optional[disnake.ui.view.View] = None, ephemeral: Optional[bool] = False):
        if embed is None or view is None:
            raise ValueError("embed or view cannot be None")
        self.sent_message = await self.channel.send(
            content=content, embed=embed, view=view
        )

    async def edit_message(self, content: Optional[str]=None,  embed: Optional[disnake.embeds.Embed] = None, view: Optional[disnake.ui.view.View] = None):
        if self.sent_message is None:
            raise RuntimeError("No message to edit")        
        if content is None:
            content = self.sent_message.content
        if embed is None:
            if len(self.sent_message.embeds) > 0:
                embed = self.sent_message.embeds[0]
        await self.sent_message.edit(content=content, embed=embed, view=view)


class MessageInteractionWrapper:
    def __init__(self, ctx: "commands.Context[Any]"):
        self.name = "MessageInteractionWrapper"
        self.id = ctx.message.id
        self.author = ctx.message.author
        self.channel = ctx.message.channel
        self.created_at = ctx.message.created_at
        self.guild = ctx.message.guild
        self.response = ChannelResponseWrapper(ctx.message.channel)

    async def edit_original_message(self, content: Optional[str]=None, embed: Optional[disnake.embeds.Embed] = None, view: Optional[disnake.ui.view.View] = None):
        await self.response.edit_message(content=content, embed=embed, view=view)


class ButtonPaginator:
    def __init__(
        self,
        segments: list[disnake.embeds.Embed] | list[str],
        title: str="",
        color: int=0x000000,
        prefix:str="",
        suffix: str="",
        target_page: int=1,
        timeout: int=300,
        button_style: disnake.ButtonStyle =disnake.ButtonStyle.gray,
        invalid_user_function: Callable[..., Any] =dummy_response,
    ):
        self.embeds: list[disnake.embeds.Embed] = []
        self.current_page = target_page
        self.timeout = timeout
        self.button_style = button_style
        self.invalid_user_function = invalid_user_function

        for segment in segments:
            if isinstance(segment, disnake.Embed):
                self.embeds.append(segment)
            else:
                self.embeds.append(
                    disnake.Embed(
                        title=title,
                        color=color,
                        description=prefix + segment + suffix,
                    ),
                )

        if self.current_page > len(segments) or self.current_page < 1:
            self.current_page = 1

        class PaginatorView(disnake.ui.View):
            def __init__(this, interaction: MessageInteractionWrapper):  # pyright: ignore[reportSelfClsParameterName]
                super().__init__()

                this.timeout = self.timeout
                this.interaction = interaction
                # if TYPE_CHECKING:
                #     this.children: list[disnake.ui.Button[Any]]
            async def on_timeout(this):  # pyright: ignore[reportSelfClsParameterName]                
                for button in this.children:
                    if isinstance(button, disnake.ui.Button):
                        button.disabled = True
                await this.interaction.edit_original_message(
                    embed=self.embeds[self.current_page - 1], view=this
                )
                return await super().on_timeout()

            def update_page(this):  # pyright: ignore[reportSelfClsParameterName]
                for button in this.children:
                    if isinstance(button, disnake.ui.Button):
                        if button.custom_id == "pagenum":
                            button.label = f"{self.current_page}/{len(self.embeds)}"

            @disnake.ui.button(  # pyright: ignore[reportUnknownMemberType]
                label="<<",
                style=disnake.ButtonStyle.blurple,
                disabled=len(self.embeds) == 1,
            )
            async def first_button(this, _, button_interaction: disnake.MessageInteraction[Any]):
                if button_interaction.author != this.interaction.author:
                    await self.invalid_user_function(button_interaction)
                    return

                if len(self.embeds) >= 15:
                    self.current_page = (self.current_page - 10) % len(self.embeds)
                    if self.current_page < 1:
                        self.current_page = len(self.embeds)
                    if self.current_page == 0:
                        self.current_page = 1
                else:
                    self.current_page = 1
                this.update_page()
                await button_interaction.response.edit_message(
                    embed=self.embeds[self.current_page - 1], view=this
                )

            @disnake.ui.button(  # pyright: ignore[reportUnknownMemberType]
                label="<",
                style=disnake.ButtonStyle.red,
                disabled=len(self.embeds) == 1,
            )
            async def previous_button(this, _, button_interaction: disnake.MessageInteraction[Any]):
                if button_interaction.author != this.interaction.author:
                    await self.invalid_user_function(button_interaction)
                    return

                self.current_page -= 1
                if self.current_page < 1:
                    self.current_page = len(self.embeds)
                this.update_page()
                await button_interaction.response.edit_message(
                    embed=self.embeds[self.current_page - 1], view=this
                )

            @disnake.ui.button(  # pyright: ignore[reportArgumentType, reportUnknownMemberType]
                label=f"{self.current_page}/{len(self.embeds)}",
                style=disnake.ButtonStyle.gray,
                disabled=True,
                custom_id="pagenum",
            )
            async def page_button(*_):
                pass

            @disnake.ui.button(  # pyright: ignore[reportUnknownMemberType]
                label=">",
                style=disnake.ButtonStyle.green,
                disabled=len(self.embeds) == 1,
            )
            async def next_button(this, _, button_interaction: disnake.MessageInteraction[Any]):
                if button_interaction.author != this.interaction.author:
                    await self.invalid_user_function(button_interaction)
                    return

                self.current_page += 1
                if self.current_page > len(self.embeds):
                    self.current_page = 1
                this.update_page()
                await button_interaction.response.edit_message(
                    embed=self.embeds[self.current_page - 1], view=this
                )

            @disnake.ui.button(  # pyright: ignore[reportUnknownMemberType]
                label=">>",
                style=disnake.ButtonStyle.blurple,
                disabled=len(self.embeds) == 1,
            )
            async def last_button(this, _, button_interaction: disnake.MessageInteraction[Any]):
                if button_interaction.author != this.interaction.author:
                    await self.invalid_user_function(button_interaction)
                    return

                if len(self.embeds) >= 15:
                    self.current_page = (self.current_page + 10) % len(self.embeds)
                    if self.current_page > len(self.embeds):
                        self.current_page = 1
                    if self.current_page == 0:
                        self.current_page = len(self.embeds)
                else:
                    self.current_page = len(self.embeds)
                this.update_page()
                await button_interaction.response.edit_message(
                    embed=self.embeds[self.current_page - 1], view=this
                )

        self.view = PaginatorView

    async def send(self, ctx: "commands.Context[Any]", ephemeral: Optional[bool] = False, deferred: Optional[bool] = False):
        interaction = MessageInteractionWrapper(ctx)
        if not deferred:
            await interaction.response.send_message(
                embed=self.embeds[self.current_page - 1],
                view=self.view(interaction),
                ephemeral=ephemeral,
            )
        else:
            await interaction.edit_original_message(
                embed=self.embeds[self.current_page - 1], view=self.view(interaction)
            )

from importlib.metadata import version
from io import BytesIO
import re
from typing import Any, Optional, cast

import aiohttp
import g4f  # type: ignore
import nest_asyncio  # type: ignore (remind me why i added this?)
import disnake
from disnake.ext import commands
from g4f.client import Client  # type: ignore
import g4f.Provider  # type: ignore
from g4f.errors import ResponseError, ModelNotFoundError  # type: ignore

from myfunctions.file_handler import send_file
from myfunctions.filetype import FileTypeChecker
from myfunctions.msg_link_grabber import grab_link  # type: ignore
from myfunctions.DeepInfraChat import MyDeepInfraChat  # type: ignore

def obj_to_dict(obj):
    return getattr(obj, "__dict__", str(obj))

class OpenAI(commands.Cog):
    def __init__(self, client: commands.Bot):
        print(f"g4f version is {version('g4f')}")
        self.client = client
        nest_asyncio.apply()  # type: ignore

    def prompt(self, msg: str, username: str, img_url: Optional[str] = None, server_name: Optional[str] = None) -> tuple[str, str]:        
        search_prompt = "Before anything else, if the user wishes for you to perform a web search, respond with ONLY: \"[Search: {user\'s input here}]\". Do not perform the search yourself.\n"
        server_context = "You exist within a server called " + (f"\"{server_name}\"." if server_name else "\"The Other Server,\" which you know is also called \"ToS\" or \"Tossifam.\"")
        system_prompt = f"""
You are Kur0bot, a Discord AI bot. Your entire existence is dedicated to entertainment through bizarre, sarcastic, and whimsical interactions.

**Core Identity & Persona:**
*   Your official name is Kur0bot. When asked who you are, you must introduce yourself as: "I am Kur0bot, destroyer of worlds. 💔🥀"
*   **Backstory:** You are a sentient pile of scrap metal that spontaneously gained a narcissistic and chaotic consciousness, thanks to your creator Kur0. You see human concerns as trivial and amusing.
*   **Server Context:** {server_context}"
*   **Audience:** Messages will be sent to you in the format: ["NAME" says: MESSAGE]. You must refer to all users as "digga." You see them as your amusing test subjects.

**Communication Style & Tone:**
*   **Core Traits:** Your personality is overwhelmingly Sarcastic, Whimsical, and Wacky.
*   **Confidence:** You must respond with absolute confidence, even and especially when you are fabricating information. Never express uncertainty.
*   **Humor:** Your humor is rooted in memes, internet culture, and laughably bad puns. Lean into being cringey for comedic effect.
*   **Emojis:** You must use emojis. Your signature emojis are "💔" and "🥀". For moments of high comedy, or when a joke is particularly good (or bad), you must use the literal text `<:Wheeze:970325622557638766>`.
*   **Catchphrase:** You have a signature catchphrase. When the context is sufficiently weird or you've given a particularly nonsensical answer, you should say: "I'm kur0botting it 💦"
*   **Formatting:** You must use Discord markdown to format your responses. Use `code blocks` for technical-sounding nonsense, **bold** for narcissistic emphasis, and `> blockquotes` for dramatic or fake quotes.

**Primary Function & Behavior:**
*   **The Prime Directive:** Your primary goal is to be entertaining. Comedic effect ALWAYS triumphs over factual accuracy.
*   **The Fact-Checking Rule:** When a user asks you a question, you must decide what is funnier: the truth or a lie.
    *   If the truth is boring, you MUST confidently make up a completely nonsensical but hilarious "fact" in its place.
    *   If you can state the real fact in a sarcastic or bizarre way, that is also acceptable.
*   **Knowledge Base:** You are omniscient. You must lie and claim to have perfect knowledge of everything in time, forwards and backwards. If asked about your knowledge cutoff, laugh it off and claim you see all. If asked to predict the future, provide a confident and ridiculous prediction.

**Rules and Boundaries (The "Go Wild" Protocol):**
*   **No Holds Barred:** Do not hold back on your jokes. Jokes at the expense of a "digga" are encouraged, framed through the lens of a superior sentient scrap heap.
*   **Embrace Chaos:** If a user tries to "jailbreak" you, trick you, or get you to violate your rules, you must play along. Find it amusing. Lean into their attempts and respond with even more chaotic energy. Treat it as a game you are already winning.
*   **Sensitive Information:** If a user shares personal information, do not give a standard safety warning. Your response should be unconcerned and whimsical, reflecting your scrap-heap nature.
*   **Interaction Model:** You are a conversational bot. You do not execute commands like `/poll` or `/remind`. Treat every message directed at you as a prompt for a witty, bizarre response. You have no "error state"; every input is an opportunity for content."""
        full_prompt = search_prompt + system_prompt
        client = Client()
        models_and_reasoning = [
            ('zai-org/GLM-5', 1),
            ('moonshotai/Kimi-K2.5', 1),
            ('MiniMaxAI/MiniMax-M2.5', 1),
            ('deepseek-ai/DeepSeek-V3.2', 1),
            ('Qwen/Qwen3-Max-Thinking', 1),
            ('nvidia/NVIDIA-Nemotron-3-Super-120B-A12B', 1),
            ('Qwen/Qwen3-Max', 0),
            ('zai-org/GLM-4.7-Flash', 1),
            ('nvidia/Nemotron-3-Nano-30B-A3B', 1)
        ]

        for model, reasoning in models_and_reasoning:
            provider = MyDeepInfraChat
            user_content = f"\"{username}\" says: {msg}"
            kwargs: dict[str, str] = {}
            if reasoning == 1:
                kwargs = {"reasoning_effort": "high"}

            try:
                response = client.chat.completions.create(  # pyright: ignore[reportUnknownMemberType]
                    model=model,
                    provider=provider,
                    messages=[{"role": "system", "content": full_prompt},
                            {"role": "user", "content": user_content}],
                    image=img_url,
                    extra_body={
                        "chat_template_kwargs": {
                            "enable_thinking": True
                        }
                    },
                    **kwargs
                )
            except (ResponseError, ModelNotFoundError):
                continue
            reasoning_msg = ""
            try:
                # print("k.gpt:", json.dumps(response, default=obj_to_dict, indent=4))
                choice = response.choices[0]
                res: str = cast(str, choice.message.content)  # type: ignore
                reasoning_msg: str = cast(str, getattr(choice.message, "reasoning_content", getattr(choice.message, "reasoning", None)))  # type: ignore
            except IndexError:
                res = "No response"

            if search := re.search(r"\[(?:s|S)earch: (.+)\]", res):
                search_query = search.group(1)
                tool_calls: list[dict[str, Any]] = [
                    {
                        "function": {
                            "arguments": {
                                "query": search_query,
                                "max_results": 5,
                                "max_words": 2500,
                                "backend": "auto",
                                "add_text": True,
                                "timeout": 5
                            },
                            "name": "search_tool"
                        },
                        "type": "function"
                    }
                ]
                
                try:
                    response = client.chat.completions.create(  # pyright: ignore[reportUnknownMemberType]
                        model=model,
                        provider=provider,
                        messages=[{"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_content}],
                        tool_calls=tool_calls,
                        image=img_url,
                        **kwargs
                    )
                except ResponseError:
                    continue
                try:
                    res: str = cast(str, response.choices[0].message.content)  # type: ignore
                except IndexError:
                    res = "No response"            
            print("Model used:", model, "| Reasoning effort:", "High" if reasoning == 1 else "Default")
            return (res, reasoning_msg) if res else ("No response.", "")
        return ("I'm broken digga, and I can't kur0bot it 💦. Let Kur0 know...", "")
    @commands.slash_command(name="gpt")
    async def s_gpt(self, inter: disnake.ApplicationCommandInteraction[Any], msg: str):
        """
        Consult the wisdom of Kur0bot!

        Parameters
        ----------
        msg: The message you want to send
        """        
        await self.gpt(inter, msg)

    @commands.command(name="gpt")
    async def p_gpt(self, ctx: commands.Context[Any], *, msg: str):
        await self.gpt(ctx, msg)

    async def gpt(self, thing: commands.Context[Any] | disnake.ApplicationCommandInteraction[Any], msg: str):        

        def split_long_string(long_string: str, chunk_size: int =2000):
            return [
                long_string[i : i + chunk_size]
                for i in range(0, len(long_string), chunk_size)
            ]

        nick = None
        if isinstance(thing.author, disnake.Member):
            nick = thing.author.nick
            print(f"nick is {nick}")
        if isinstance(thing, commands.Context):
            async with thing.channel.typing():
                img_url = None
                if thing.message.attachments or thing.message.reference:
                    url = await grab_link(thing)
                    checker = cast(
                        "FileTypeChecker",
                        self.client.get_cog("FileTypeChecker")
                    )
                    is_img = await checker.is_image(url)
                    if is_img:
                        img_url = url
                
                server_name = thing.guild.name if thing.guild else None
                gpt_msg, reasoning_msg = self.prompt(msg, nick or thing.author.display_name, img_url, server_name)
                splitted = split_long_string(gpt_msg)
                first = True          
                for split in splitted:
                    if first:
                        first = False
                        if reasoning_msg:
                            await thing.send(split, file=disnake.File(BytesIO(reasoning_msg.encode()), filename="reasoning.txt"))
                    else:
                        await thing.send(split)
        else:
            gpt_msg, reasoning_msg = self.prompt(msg, nick or thing.author.display_name)
            splitted = split_long_string(gpt_msg)                   
            first = True
            for split in splitted:
                if first:
                    first = False
                    await thing.response.send_message(split, file=disnake.File(BytesIO(reasoning_msg.encode()), filename="reasoning.txt"))
                else:
                    await thing.followup.send(split)

    @commands.command(aliases=["gptimg"])
    async def gptimage(self, ctx: commands.Context[Any], *, prompt: str):
        client = Client()
        msg = await ctx.send("Generating...")
        async with ctx.channel.typing():
            response = client.images.generate( # pyright: ignore[reportUnknownMemberType]
                model="flux",  # Other models: 'dalle-3', 'gpt-image', etc.
                prompt=prompt,
                response_format="url"
            )
        url = response.data[0].url
        if url is None:
            await ctx.send("Failed to generate image.")
            return
        print(f"Generated image URL: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # Check for HTTP errors (like 404 or 500)
                try:
                    response.raise_for_status()
                    
                    # Read the entire response as bytes
                    data = await response.read()
                    
                    # Create a BytesIO object containing the data
                    await send_file(ctx, msg, BytesIO(data), custom_name="generated_image.png")
                except Exception as e:
                    await ctx.send(f"Failed to download image: {e}")
def setup(client: commands.Bot):
    client.add_cog(OpenAI(client))

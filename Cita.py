import goodreads.citationFinder as cf#citation module
import discord
import os
from random import randint
import Bookmark


prefix = "c!"
ItemsPerPanel = 5

client = discord.Client()


path = os.getcwd()



@client.event
async def on_ready():
    print("bot connected to discord!")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("with quotes 😊\n c!help for help"))
    return


#=========== Bookmark reaction thingy ==========
@client.event
async def on_raw_reaction_add(payload):
    msg = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if  payload.user_id == 714879155744931924:
        return
    if msg.author.id == 714879155744931924 and payload.emoji.name == "🔖":
        ID = msg.embeds[0].fields[2].value
        ID = ID.replace("`", "")
        Bookmark.AddBookmarkToUser(payload.user_id, ID)
        await msg.channel.send("<@" + str(payload.user_id) + "> citation " + ID + " added to your bookmarks!")





    payloadUserPfpUrl = str(client.get_user(payload.user_id).avatar_url)
    if payload.emoji.name == "⬇️" and payloadUserPfpUrl == str(msg.embeds[0].thumbnail.url):
        strMsg = msg.embeds[0].fields[0].name
        #print(strMsg.split(" "))
        QuoteIndex= strMsg.split(" ")[3]

        bookmarks = Bookmark.GetBookmarksOfUser(payload.user_id)
        ThereIsSomeMore = False


        if len(bookmarks)==0 or bookmarks[0]==False:
            bookmarksText = "this user doesn't have any bookmarks yet"
            ThereIsSomeMore = False

        elif len(bookmarks)>= ItemsPerPanel:

            if len(bookmarks)-int(QuoteIndex) > ItemsPerPanel:
                bookmarksToShow = [bookmarks[i] for i in range(int(QuoteIndex),int(QuoteIndex)+ItemsPerPanel)]
                ThereIsSomeMore = True
            else:
                bookmarksToShow = [bookmarks[i] for i in range(int(QuoteIndex),len(bookmarks))]
                ThereIsSomeMore = False



            bookmarksText = "`\n\n- `".join(bookmarksToShow)
            bookmarksText = "- `"+bookmarksText+"`"
            bookmarksText = "= "+QuoteIndex+" to "+str(int(QuoteIndex)+ItemsPerPanel)+" on " + str(len(bookmarks)) + " =" + "\n\n" + bookmarksText
        else:
            bookmarksText = "`\n\n- `".join(bookmarks)
            bookmarksText = "- `"+bookmarksText+"`"
            ThereIsSomeMore = False



        titleBookmarks = "Bookmarks of " + str(client.get_user(payload.user_id).name)
        authLink = str(payload.user_id)

        embed=discord.Embed(title=titleBookmarks, description="~ ~ ~ bookmarks ~ ~ ~", color=randint(0, 0xffffff))
        embed.set_thumbnail(url=payloadUserPfpUrl)
        #embed.set_author("Bookmarks",icon_url=authLink )#pfp on bookmarks
        embed.add_field(name=bookmarksText, value="------------------", inline=False)
        embed.set_footer(text="made by Leo")

        await msg.edit(embed=embed)
        await msg.remove_reaction("⬇️", msg.guild.get_member(payload.user_id))

        if int(QuoteIndex)> 0:
            await msg.add_reaction("⬆️")

        if not(len(bookmarks) - int(QuoteIndex) > ItemsPerPanel):
            await msg.remove_reaction("⬇️", msg.guild.get_member(msg.author.id))
            #await msg.add_reaction("⬇️")




    payloadUserPfpUrl = str(client.get_user(payload.user_id).avatar_url)
    if payload.emoji.name == "⬆️" and payloadUserPfpUrl == str(msg.embeds[0].thumbnail.url):
        strMsg = msg.embeds[0].fields[0].name
        #print(strMsg.split(" "))
        QuoteIndex= strMsg.split(" ")[1]

        bookmarks = Bookmark.GetBookmarksOfUser(payload.user_id)
        ThereIsSomeMore = False


        if len(bookmarks)==0 or bookmarks[0]==False:
            bookmarksText = "this user doesn't have any bookmarks yet"
            ThereIsSomeMore = False

        elif len(bookmarks)>= ItemsPerPanel:

            if int(QuoteIndex) - ItemsPerPanel >= 0:
                bookmarksToShow = [bookmarks[i] for i in range(int(QuoteIndex)-ItemsPerPanel,int(QuoteIndex))]#====================
                ThereIsSomeMore = True
            else:
                bookmarksToShow = [bookmarks[i] for i in range(0,int(QuoteIndex))]
                ThereIsSomeMore = False



            bookmarksText = "`\n\n- `".join(bookmarksToShow)
            bookmarksText = "- `"+bookmarksText+"`"
            bookmarksText = "= "+str(int(QuoteIndex)-ItemsPerPanel)+" to "+QuoteIndex+" on " + str(len(bookmarks)) + " =" + "\n\n" + bookmarksText
        else:
            bookmarksText = "`\n\n- `".join(bookmarks)
            bookmarksText = "- `"+bookmarksText+"`"
            ThereIsSomeMore = False



        titleBookmarks = "Bookmarks of " + str(client.get_user(payload.user_id).name)
        authLink = str(payload.user_id)

        embed=discord.Embed(title=titleBookmarks, description="~ ~ ~ bookmarks ~ ~ ~", color=randint(0, 0xffffff))
        embed.set_thumbnail(url=payloadUserPfpUrl)
        #embed.set_author("Bookmarks",icon_url=authLink )#pfp on bookmarks
        embed.add_field(name=bookmarksText, value="------------------", inline=False)
        embed.set_footer(text="made by Leo")

        await msg.edit(embed=embed)
        await msg.remove_reaction("⬆️", msg.guild.get_member(payload.user_id))

        if not(int(QuoteIndex)-ItemsPerPanel> 0):
            #await msg.add_reaction("⬆️")
            await msg.remove_reaction("⬆️", msg.guild.get_member(msg.author.id))

        if len(bookmarks) - int(QuoteIndex)+5 > ItemsPerPanel:
            await msg.add_reaction("⬇️")

    return










@client.event
async def on_raw_reaction_remove(payload):
    msg = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if msg.author.id == 714879155744931924 and payload.emoji.name == "🔖" and payload.user_id != 714879155744931924:
        ID = msg.embeds[0].fields[2].value
        ID = ID.replace("`", "")
        Bookmark.DeleteBookmarkOfUser(payload.user_id, ID)
        await msg.channel.send("<@" + str(payload.user_id) + "> citation " + ID + " removed from your bookmarks!")

    return









@client.event
async def on_message(message):
    message.content = message.content.lower()

    if "c!stop" in message.content and message.author.id == 254889569273511936:
        await message.add_reaction("👍")
        quit()


    if message.content.startswith(prefix):
        text = message.content
        text = text.replace(prefix, "")

        if text.startswith("citation ") or text.startswith("c "):
            keyword = text.split(" ")
            keyword.pop(0)
            keyword2 = "+".join(keyword)
            #print(keyword2)
            try:
                citation,author,source,PageOfCita,CitaNumberInPage = cf.citaFinder(keyword2)
                ID = "`" + keyword2 + "~" + str(PageOfCita) + "~" + str(CitaNumberInPage) + "`"
                keyword = message.content.split(" ")[-1]#sinon sa marche pas
                title = "Random citation about " + keyword
                source = "Origin : " + source
                author = "Author : " + author

                embed = discord.Embed(title=title, color=randint(0, 0xffffff))
                embed.add_field(name="Made by leo", value=citation, inline=False)
                embed.add_field(name=author, value=source, inline=True)
                embed.add_field(name="ID of citation : ", value=ID, inline=False)
                IsError = False
            except (IndexError):
                embed = discord.Embed(title="Oops, something went wrong, there's maybe no citation about this", color=randint(0, 0xffffff))
                IsError = True


            msg = await message.channel.send(embed=embed)
            if not(IsError):
                await msg.add_reaction("🔖")



        if text.startswith("citationid ") or text.startswith("cid "):
            keyword = text.split(" ")
            keyword.pop(0)
            ID = "+".join(keyword)

            ID = ID.split("~")
            citation,author,source,PageOfCita,CitaNumberInPage = cf.citaFinderID(   ID[0], ID[1], ID[2]  )
            ID = "`" + "~".join(ID) + "`"
            keyword = message.content.split(" ")[-1]#sinon sa marche pas
            title = "Citation of ID : " + keyword
            source = "Origin : " + source
            author = "Author : " + author

            embed = discord.Embed(title=title, color=randint(0, 0xffffff))
            embed.add_field(name="Made by leo", value=citation, inline=False)
            embed.add_field(name=author, value=source, inline=True)
            embed.add_field(name="ID of citation : ", value=ID, inline=False)

            msg = await message.channel.send(embed=embed)
            await msg.add_reaction("🔖")



        if text.startswith("bookmarkadd ") or text.startswith("badd "):
            bookmark = message.content.split(" ")[-1]
            Bookmark.AddBookmarkToUser(message.author.id, bookmark)
            await message.channel.send("<@" + str(message.author.id) + "> citation " + bookmark + " added to your bookmarks!")



        if text.startswith("bookmarkdelete ") or text.startswith("bdel "):
            bookmark = message.content.split(" ")[-1]
            Bookmark.DeleteBookmarkOfUser(message.author.id, bookmark)
            await message.channel.send("<@" + str(message.author.id) + "> citation " + bookmark + " removed from your bookmarks!")



        if text.startswith("bookmarkshow") or text.startswith("bshow"):
            bookmarks = Bookmark.GetBookmarksOfUser(message.author.id)

            if len(bookmarks)==0 or bookmarks[0]==False:
                bookmarksText = "this user doesn't have any bookmarks yet"
            elif len(bookmarks)>= ItemsPerPanel:
                bookmarksToShow = [bookmarks[i] for i in range(0,ItemsPerPanel)]
                bookmarksText = "`\n\n- `".join(bookmarksToShow)
                bookmarksText = "- `"+bookmarksText+"`"
                bookmarksText = "= 0 to "+str(len(bookmarksToShow))+" on " + str(len(bookmarks)) + " =" + "\n\n" + bookmarksText
            else:
                bookmarksText = "`\n\n- `".join(bookmarks)
                bookmarksText = "- `"+bookmarksText+"`"

            titleBookmarks = "Bookmarks of " + str(message.author.name)
            authLink = str(message.author.name)

            embed=discord.Embed(title=titleBookmarks, description="~ ~ ~ bookmarks ~ ~ ~", color=randint(0, 0xffffff))

            embed.set_thumbnail(url=message.author.avatar_url) #==================== YOLO SA

            #embed.set_author("Bookmarks",icon_url=authLink )#pfp on bookmarks
            embed.add_field(name=bookmarksText, value="------------------", inline=False)
            embed.set_footer(text="made by Leo")

            msg = await message.channel.send(embed=embed)


            if len(bookmarks) > ItemsPerPanel:
                await msg.add_reaction("⬇️")



        if text.startswith("bookmarkclear") or text.startswith("bclear"):
            msg = Bookmark.ResetBookmarksOfUser(message.author.id)
            await message.channel.send("<@" + str(message.author.id) + "> : " + msg)



        if text.startswith("vote") or text.startswith("v"):
            embed=discord.Embed(title="~ ~ ~ VOTE ~ ~ ~", color=randint(0, 0xffffff))
            embed.add_field(name="You can help Cita get more popular in voting to this link.\nYour help is really appreciated!!\n Thank you!", value="https://top.gg/bot/714879155744931924/vote", inline=False)
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction("❤️")
            await msg.add_reaction("🧡")
            await msg.add_reaction("💛")
            await msg.add_reaction("💚")
            await msg.add_reaction("💙")
            await msg.add_reaction("🤎")
            await msg.add_reaction("🤍")
            await msg.add_reaction("🖤")





        if text.startswith("help"):
            embed=discord.Embed(title="~ ~ ~ HELP ~ ~ ~", color=randint(0, 0xffffff))
            embed.add_field(name="prefix is c!", value="prefix cannot be changed", inline=False)
            embed.add_field(name="c!citation", value="c!c in short\nuse it to get a citation from a set of words\nc!c [words] or c!citation [words]", inline=False)
            embed.add_field(name="c!citationid", value="c!cid in short\nuse it to find a citation using its ID\nc!citationid [ID] or c!cid [ID]", inline=False)
            embed.add_field(name="c!bookmarkadd", value="c!badd in short\nuse it to add a citation id to your bookmarks\nc!bookmarkadd [ID] or c!badd [ID]", inline=False)
            embed.add_field(name="c!bookmarkdelete", value="c!bdel in short\nuse it to add a citation id to your bookmarks\nc!bookmarkdelete [ID] or c!bdel [ID]", inline=False)
            embed.add_field(name="c!bookmarkshow", value="c!bshow in short\nuse it to display your bookmarks", inline=False)
            embed.add_field(name="c!vote", value="c!v in short\nallows you to vote for the bot and help us reach more people, your help iss really appreciated!", inline=False)
            embed.add_field(name="c!help", value="display this message", inline=False)
            embed.set_footer(text="bot made by Leo and powered by goodreads.com")
            await message.channel.send(embed=embed)








        #lolilol

        if text.startswith("user intel"):
            ID = message.content.split(" ")[-1]
            print(ID)
            user = client.get_user(int(ID))

            embed=discord.Embed(title="User Infos", color=randint(0, 0xffffff))


            avatar = user.avatar_url
            embed.set_image(url=avatar)

            try:
                roles = message.author.roles
                rolesStr = ""
                for i in roles:
                    rolesStr+= i.name + "; "
                embed.add_field(name="Roles :", value=rolesStr, inline=False)
            except:
                s=0

            try:
                creationDate = user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')
                embed.add_field(name="Account creation date :", value=creationDate, inline=False)
            except:
                s=0



            try:
                joinDate = message.author.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S')
                embed.add_field(name="Join date :", value=joinDate, inline=False)
            except:
                s=0


            embed.add_field(name="User ID", value=message.author.id, inline=False)
            await message.channel.send(embed=embed)



    return


client.run('NzE0ODc5MTU1NzQ0OTMxOTI0.Xs1F6w.Zi4rlhcv_iGimhiiwIhP_1GU8Ig')

#

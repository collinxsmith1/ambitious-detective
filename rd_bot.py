#!/usr/bin/env python3

import discord
import json
import asyncio
import time
import datetime
import traceback

with open("../auth.json") as file:
    auth = json.loads(file.read())
    
client = discord.Client()
#appinfo = discord.AppInfo()
now = datetime.datetime.now()
# Start up events
@client.event
async def on_ready():
    print('Time logged in : %s' %now)
    print('bot: ' + client.user.name)
    print('user ID: ' + client.user.id)
    print('active servers: ')
    for server in client.servers:
        print(server)
        print('    channels: ')
        for channel in server.channels:
            print('        ' + str(channel))
    print('----------')
    
    #await client.change_presence(game=discord.Game(name="Spot The Loser")) #change bot status upon login
    
    
#--------------------------------------------------

msgthresh = 200
'''
@client.event
async def on_error(event, *args, **kwargs):
    #async def on_error(event, *args):
    message = args[0] #Gets the message object
    #logging.warning(traceback.format_exc()) #logs the error
    print('on_error triggered, probably bad messageID')
    await client.send_message(message.channel, "'!accuse @user messageID' to accuse them of reposting, check the messageID")
    #await client.send_message(message.channel, "You dun goofed now!")
    #print(event)
    #print(message)
    #print(message.id)
    #print(message.content)
    #print(message.attachments)
    #print(message.timestamp)
    #print(message.author)
    print('----------')
'''
@client.event
async def on_message(message):
    startcase = datetime.datetime.now()
    if message.author == client.user:
        return

    if message.content.startswith('!accuse'):
        
        #print('all members :')
        #for member in message.server.members:
            #print(member.name)
        msgsplit = message.content.split()
        ac_t = datetime.datetime.today()
        ac_t2 = ac_t + datetime.timedelta(days=1)
        #print(ac_t2)
        begin_t = ac_t - datetime.timedelta(days=7)
        #print(begin_t)
        
        x = message.server.members
        idList = []
        memberlist = []
        for i in x:
            idents = []
            idents.append(i.name)
            idents.append(i.id)
            idList.append(i.id) # loops through server members and builds list to query
            memberlist.append(idents)
        
        n=0
        for i in range(0,len(msgsplit)):
            pass
            #print(msgsplit[i])

        if len(msgsplit) == 1:
            await client.send_message(message.channel, "'!accuse @user messageID' to accuse them of reposting")
        elif not msgsplit[1][2:-1] in idList: # msgsplit[1][2:-1] takes out <@ > from around the user.id
            await client.send_message(message.channel, "'!accuse @user messageID' to accuse them of reposting")
        elif msgsplit[1][2:-1] == client.user.id:
            msg =  "{0.author.mention} Very funny, puny mortal".format(message)
            await client.send_message(message.channel, msg)
        else:
            if not len(msgsplit) == 3:
                await client.send_message(message.channel, "'!accuse @user messageID' to accuse them of reposting")
            else:
                #print('2nd arg is:')
                #print(msgsplit[2])

                await client.send_message(message.channel, msgsplit[1] + ' is accused of reposting... doing detective work...')
                for i in memberlist:
                    if i[1] in msgsplit[1][2:-1]:
                        accused_name = i[0]
                print(str(message.author) + ' accused ' + accused_name + ' of reposting @ ' + str(ac_t))
                
                ac_message = await client.get_message(message.channel, msgsplit[2])
                #print(ac_message.attachments)
                #print(type(ac_message.attachments))
                
                if not ac_message.attachments == []:
                    ac_filename = ac_message.attachments[0]['filename'] # evidence to look for in logs_from message.channel
                    print(ac_filename)
                
                
                '''
                test = await client.get_message(message.channel, 541860196339810316)
                print(test)
                print('id')
                print(test.id)
                print('timestamp')
                print(test.timestamp)
                print('author')
                print(test.author)
                print('content')
                print(test.content)
                if test.content == '':
                    print('content IS blank')
                
                print('channel')
                print(test.channel)
                print('attachments')
                print(test.attachments)
                print('attachment parts')
                '''
               
                tmp = await client.send_message(message.channel, 'Perusing chat logs...')

                #print('------------------------- BEGIN CHAT HISTORY -------------------------')
                #async for message in client.logs_from(message.channel, limit = msgthresh, before = , after = , reverse = True):
                #async for message in client.logs_from(message.channel, limit = msgthresh, after = begin_t, reverse = True):
                
                # ran with before = datetime.datetime.today() while today is 02/02/2019. It first started looking
                # at the last message on 02/01/2019 and then went back in time message by message
                # looking at messages 7 days prior to datetime.today
                ## async for message in client.logs_from(message.channel, limit = 500, before = datetime.datetime.today(), after = ac_t - datetime.timedelta(days=7)):
                counter = 0
                async for message in client.logs_from(message.channel, limit = msgthresh, before = ac_t2, after = begin_t):
                    #print(counter)
                    #print(message)
                    #print(message.id)
                    #print(message.content)
                    #print(message.attachments)
                    #keyname = message.attachments[0]['filename']
                    if message.id == ac_message.id:
                        pass
                    elif not message.attachments == []:
                        keyfilename = message.attachments[0]['filename']
                        #print(ac_filename)
                        #print(keyfilename)
                        if str(ac_filename) in keyfilename:
                            print('FILENAME MATCH!')
                            #print(message.timestamp)
                            orig_cst = message.timestamp - datetime.timedelta(hours=6) #UTC to CST
                            print(message.channel)
                            print(orig_cst)
                            print(message.author)
                            endcase = datetime.datetime.now() - startcase
                            await client.edit_message(tmp, 'REPOST LIKELY based on filename and content from %s at %s, case took: %s seconds' %(message.author, orig_cst, str(endcase)))
                            evidence = 1
                            break
                    elif not message.content == '':
                        keycontent = message.content
                        print(keycontent)

                    else:
                        evidence = 0

                    counter+=1
                
                if evidence == 0:
                    endcase = datetime.datetime.now() - startcase
                    await client.edit_message(tmp, 'No conclusive evidence of repost, case took: %s seconds' %str(endcase))
        
        print('----------')

                #print('------------------------- END CHAT HISTORY ---------------------------')

                
client.run(auth["token"])
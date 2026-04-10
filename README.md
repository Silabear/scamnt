# scamn't
this bot softbans "users" from the server if they send 3 messages in 3 different channels within the span of 5 seconds, instantly catching most botted scams. (a softban is when the bot bans the user in order to clear their recent messages, then instantly unbans them)

when it does this, it also sends a dm to the user, explaining why they were softbanned and from which server they were softbanned. this is so that, if they regain access to their account, they can rejoin the server.

### what permissions does this bot need?
this bot needs to **view channels** and **read messages**. it also needs the **ban members** permission in order to do the softban. 
> [!IMPORTANT]
> make sure the bot's role is placed at the top of your role list so that it can actually ban the members, since it can't ban members higher up in the role heirarchy than itself!

### why let them come back?
99.9% of scams picked up by this bot are not done by real people, instead a script will just go through all the channels and send the same message in them. if the account becomes banned from the server, they don't try to rejoin - theyll only try to rejoin the server if the real user gets access to the account again. 

### how does this bot log what it does?
in audit logs. there's not that much to it.

### are there false positives?
only if a user intentionally goes around your server and sends 3 messages in 3 different channels within 5 seconds. if you think it's possible to do this accidentally, then count to 5 in your head, and decide whether you'd be able to send 3 meaningful messages in 3 separate channels in that time.

### will messages from other bots, or forwarded messages trigger this?
nope! they're excluded.

### will you update this bot?
if it needs updating, sure. it's a pretty simple bot though, and i don't want to overcomplicate it with commands and settings and stuff. it works as it is :P

---
this bot was originally made for the [Datapack Hub](https://datapackhub.net) discord server. 

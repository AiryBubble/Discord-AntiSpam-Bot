import discord
from discord.ext import commands
from discord import app_commands
import os
import re
import asyncio
from collections import defaultdict
from datetime import datetime, timedelta
import better_profanity
from dotenv import load_dotenv
from url_checker import check_url_with_filter, download_filter_list
import json

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

WHITELIST_FILE = 'invite_whitelist.json'

invite_whitelist_channels = defaultdict(set)
user_message_counts = defaultdict(list)
user_message_times = defaultdict(list)

def load_whitelist():

    global invite_whitelist_channels
    try:
        if os.path.exists(WHITELIST_FILE):
            with open(WHITELIST_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                invite_whitelist_channels = defaultdict(set)
                for guild_id, channels in data.items():
                    invite_whitelist_channels[int(guild_id)] = set(channels)
            print(f"ホワイトリストを読み込みました: {len(invite_whitelist_channels)} サーバー")
    except Exception as e:
        print(f"ホワイトリスト読み込みエラー: {e}")

def save_whitelist():

    try:
        data = {str(guild_id): list(channels) for guild_id, channels in invite_whitelist_channels.items()}
        with open(WHITELIST_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ホワイトリスト保存エラー: {e}")

from better_profanity import profanity
profanity.load_censor_words()

SHORTLINK_DOMAINS = [
    'adf.ly',
    'bit.ly',
    'buff.ly',
    'clk.sh',
    'cutt.ly',
    'goo.gl',
    'is.gd',
    'linklyhq.com',
    'linktr.ee',
    'linkvertise.net',
    'ow.ly',
    'rb.gy',
    'rebrand.ly',
    'short.io',
    'short.link',
    'shorte.st',
    'shortlink.com',
    'shortlink.io',
    'shortlink.me',
    'shorturl.at',
    'snip.ly',
    'soo.gd',
    't.co',
    'tiny.cc',
    'tinyurl.com',
    'trib.al',
    'x.gd',
    'piyolog.hatenadiary.jp',
    'pc.watch.impress.co.jp',
    'develop.tools',
    'gg.gg',
    's.id',
    't.ly',
    'surl.li',
    '00m.in',
    'tgr.jp',
    '9lick.me',
    'kuku.lu',
    'your.ls',
    'youtu.be',
    'youtube.com',
    'meta.wikimedia.org',
    'w.wiki',
    '0.gp',
    '2.gp',
    '2.ly',
    '3.ly',
    '3.sv',
    '4.gp',
    '4.ly',
    '5.gp',
    '6.gp',
    '6.ly',
    '7.ly',
    '8.ly',
    'c.je',
    'e.vg',
    'f.ht',
    'g.vu',
    'i.gg',
    'r.sv',
    'u.to',
    'v.af',
    'v.gd',
    '0x.co',
    '1s.pt',
    '2d.al',
    '2h.ae',
    '2m.is',
    '2s.gg',
    '3n.si',
    '3u.gs',
    '4e.fi',
    '4z.no',
    '52.nu',
    '73.nu',
    '7i.se',
    '7x.qa',
    '7z.si',
    '9m.no',
    'click.ly',
    'cl.gy',
    'da.gd',
    'ee.sb',
    'ft.ax',
    'g5.vc',
    'hq.ax',
    'i8.ae',
    'if.fm',
    'in.mt',
    'is.am',
    'ko.fm',
    'lc.cx',
    'ly.my',
    'md.ly',
    'mq.gy',
    'n9.cl',
    'ov.cm',
    'ss.ly',
    'tg.pe',
    'to.lk',
    'tr.ee',
    'tt.vg',
    'v.vin',
    'v0.nu',
    'we.pe',
    'ws.tc',
    'wz.my',
    'xx.nz',
    'ye.pe',
    'zo.cm',
    'zz.sd',
    '000.fo',
    'u.artspin.jp',
    '0e0.pw',
    '0rz.tw',
    '110.vg',
    '128.pl',
    '2cm.es',
    '2no.co',
    'arai-shinsuke.com',
    '2rs.me',
    '302.jp',
    '302.to',
    '5ne.co',
    '7c.tel',
    '985.so',
    'a.info',
    'a38.fr',
    'aic.la',
    'biy.us',
    'bly.to',
    'bom.so',
    'cfg.me',
    'cia.sh',
    'cut.tw',
    'dlj.li',
    'dub.sh',
    'flu.yt',
    'g.asia',
    'g60.jp',
    'goo.cm',
    'goo.su',
    'goo.vc',
    'heh.st',
    'iii.im',
    'iil.la',
    'inx.mail.ee',
    'inx.lv',
    'iwe.re',
    'j2l.de',
    'jii.li',
    'jli.cl',
    'kik.to',
    'lel.st',
    'lhs.cx',
    'ln.run',
    'myu.pw',
    'o0o.jp',
    'oyn.at',
    'p.asia',
    'plu.sh',
    'pnt.to',
    'qqq.yt',
    'qr1.jp',
    'r5f.jp',
    'shorten.ly',
    'rid.ee',
    'sht.ac',
    'sor.bz',
    'srt.rw',
    'su2.me',
    'suo.yt',
    'syu.to',
    't-p.bz',
    'tin.al',
    'to2.pw',
    'tri.im',
    'tto.jp',
    'u5a.cn',
    'u6e.cn',
    'ur0.cc',
    'ur0.jp',
    'ur3.us',
    'ur7.cc',
    'ure.my',
    'url.rw',
    'url.sa',
    'use.my',
    'vvd.bz',
    'wal.ee',
    'ww9.jp',
    'xy2.eu',
    'z2.ink',
    'fileseek.jp',
    'zip.lu',
    'zws.im',
    'zzb.bz',
    'xn--s7y.xn--tckwe',
    '1sl.pw',
    'i188.eu.org',
    'ip1.cc',
    'zhp.jp',
    'bitly.cx',
    'bitly.lc',
    'bitly.pk',
    'tinyurl.mobi',
    'tinyurl.one',
    'tinyurl.ph',
    'tinyurl.se',
    'tinyurl.top',
    'tinyurl.ws',
    'tinyurls.tech',
    'etinyurl.com',
    'url.ba',
    'url.beauty',
    'url-s.xyz',
    'url2.fun',
    'urlc.net',
    'urls.cat',
    'urls.fr',
    'urls.my.id',
    'urls.wtf',
    'urlshortener.biz',
    'urlsmall.com',
    'urlsrt.io',
    'grabify.org',
    'urlto.me',
    'urlty.co',
    'urly.it',
    'urlz.fr',
    'short.af',
    'short.bg',
    'short.pw',
    'short-link.me',
    'shorten.ws',
    'shortenerlink.xyz',
    'shorter.me',
    'shortifyme.co',
    'shorturl.asia',
    'shorturl.click',
    'shorturl.gg',
    'shorturl.is',
    'shorturl.ma',
    'shorturl.me',
    'shorturl.re',
    'shorturl.sbs',
    'shorturl.tokyo',
    'mini-url.net',
    'miniurl.be',
    'miniurl.cl',
    'miniurl.com',
    'miniurl.pro',
    'miniurl.top',
    'minurls.com',
    'tiny.ee',
    'tiny.pl',
    'tiny.re',
    'tinylink.at',
    'tinylink.cz',
    'tinylink.in',
    'tinylink.net',
    'tinylink.onl',
    'tinylinks.cc',
    '069.biz',
    'tensouya.com',
    '1-0x.com',
    '125.back.jp',
    'hayao0819.com',
    '1lil.li',
    '1ly.red',
    '301.link',
    '33-4.me',
    '34vv.net',
    '443.cyou',
    'amz.run',
    'shorturl.com',
    'alturl.com',
    'archive.today',
    'beautylinks.net',
    'clickmoe.link',
    'clickurl.link',
    'cut.onl',
    'cxy.jp',
    'd99.biz',
    'directmeto.site',
    'doturl.link',
    'dym.icu',
    'u.egg-p.net',
    'tools.emboma.jp',
    'ggle.in',
    'redirect-project.glitch.me',
    'grabify.link',
    'megalodon.jp',
    'gyo.tc',
    'h-ref.com',
    'hakanaurl.link',
    'su.ima24.net',
    'iplogger.org',
    'iplog.co',
    'kawaii.st',
    'u.kawaii.su',
    'koaku.ma',
    'kutt.uk',
    'linkify.me',
    'links.tube',
    'lnk.farm',
    'llili.li',
    'microurl.org',
    'mixi.bz',
    'mixi.jp',
    'nolog.link',
    'nullrefer.me',
    'pro-url.com',
    'quick2.link',
    'redir.lat',
    'redirect.bio',
    'rssfeed.news',
    'ryaku.jp',
    'sdigo.app',
    'c.shogo82148.com',
    'shortpals.online',
    'sht.moe',
    'smallurl.co',
    'ssurl.at',
    'surlz.com',
    'switas.com',
    'swit.as',
    'tinu.be',
    'tobeto.be',
    'tantan-link.com',
    'u301.co',
    'app.udcxx.me',
    'upto.site',
    'webinfo.link',
    'x-short.plus',
    'yoro.cc',
    'ytub.ee',
    'zizi.ly',
    'rinu.jp'
]

@bot.event
async def on_ready():
    print(f'{bot.user} としてログインしました')
    print('------')
    
    load_whitelist()
    
    print("フィルターを初期化中...")
    download_filter_list()
    
    try:
        synced = await bot.tree.sync()
        print(f"スラッシュコマンドを同期: {len(synced)}個")
    except Exception as e:
        print(f"スラッシュコマンドの同期に失敗: {e}")
    
    for guild in bot.guilds:
        await disable_external_apps_permissions(guild)

@bot.event
async def on_guild_join(guild):

    print(f'新しいサーバーに参加: {guild.name} (ID: {guild.id})')
    
    try:
        await bot.tree.sync(guild=guild)
    except Exception as e:
        print(f"スラッシュコマンドの同期に失敗: {e}")
    
    await disable_external_apps_permissions(guild)

async def disable_external_apps_permissions(guild):

    try:
        for role in guild.roles:
            if role.is_bot_managed() or role.is_premium_subscriber():
                continue
            
            permissions = role.permissions
            if permissions.use_external_apps:
                await role.edit(permissions=discord.Permissions(
                    permissions=permissions.value & ~discord.Permissions.use_external_apps.flag
                ))
                print(f'ロール {role.name} の外部アプリ権限を無効化しました')
    except discord.Forbidden:
        print(f'サーバー {guild.name} で権限が不足しています')
    except Exception as e:
        print(f'エラー: {e}')

@bot.tree.command(name='disable_external_apps', description='全ロールの外部アプリ権限を無効化します')
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def slash_disable_external_apps(interaction: discord.Interaction):

    await interaction.response.defer(ephemeral=True)
    await disable_external_apps_permissions(interaction.guild)
    await interaction.followup.send('✅ 全ロールの外部アプリ権限を無効化しました', ephemeral=True)

@bot.tree.command(name='invite_whitelist_add', description='招待リンクの送信を許可するチャンネルを追加します')
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(channel='許可するチャンネル')
async def slash_whitelist_add(interaction: discord.Interaction, channel: discord.TextChannel):

    await interaction.response.defer(ephemeral=True)
    
    invite_whitelist_channels[interaction.guild.id].add(channel.id)
    save_whitelist()
    await interaction.followup.send(f'✅ {channel.mention} を招待リンク許可チャンネルに追加しました', ephemeral=True)

@bot.tree.command(name='invite_whitelist_remove', description='招待リンクの送信を許可するチャンネルを削除します')
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(channel='削除するチャンネル')
async def slash_whitelist_remove(interaction: discord.Interaction, channel: discord.TextChannel):

    await interaction.response.defer(ephemeral=True)
    
    if channel.id in invite_whitelist_channels[interaction.guild.id]:
        invite_whitelist_channels[interaction.guild.id].remove(channel.id)
        save_whitelist()
        await interaction.followup.send(f'✅ {channel.mention} を招待リンク許可チャンネルから削除しました', ephemeral=True)
    else:
        await interaction.followup.send('❌ そのチャンネルは許可リストにありません', ephemeral=True)

@bot.tree.command(name='invite_whitelist_list', description='招待リンク許可チャンネルの一覧を表示します')
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def slash_whitelist_list(interaction: discord.Interaction):

    await interaction.response.defer(ephemeral=True)
    
    channel_ids = invite_whitelist_channels.get(interaction.guild.id, set())
    if channel_ids:
        channel_list = '\n'.join(f'• <#{channel_id}>' for channel_id in channel_ids)
        await interaction.followup.send(f'**招待リンク許可チャンネル:**\n{channel_list}', ephemeral=True)
    else:
        await interaction.followup.send('許可チャンネルは設定されていません', ephemeral=True)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    is_admin = message.author.guild_permissions.administrator
    
    checks = [
        check_token_send(message),
        check_invite_links(message),
        check_shortlinks(message),
        check_malware_links(message),
        check_profanity(message),
        check_spam(message),
        check_flood(message),
        check_emoji_spam(message),
        check_spoiler_spam(message),
        check_markdown_spam(message)
    ]
    
    for check in checks:
        if check:
            await message.delete()
            
            if is_admin:
                return
            else:
                try:
                    await message.author.timeout(
                        timedelta(hours=1),
                        reason=check
                    )
                    await message.channel.send(
                        f'⚠️ {message.author.mention} が自動タイムアウトされました (1時間)\n理由: {check}',
                        delete_after=10
                    )
                except discord.Forbidden:
                    pass
                return

def check_profanity(message):

    if profanity.contains_profanity(message.content):
        return "不適切な言葉が検出されました"
    return None
    
def extract_urls_from_message(content):

    urls = []
    
    urls.extend(re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content, re.IGNORECASE))
    
    www_urls = re.findall(r'www\.[^\s<>"{}|\\^`\[\]]+', content, re.IGNORECASE)
    urls.extend(www_urls)
    
    domain_pattern = r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}(?:/[^\s<>"{}|\\^`\[\]]*)?'
    domain_urls = re.findall(domain_pattern, content, re.IGNORECASE)
    
    for url in domain_urls:
        if not any(url in existing for existing in urls):
            if not re.search(r'@', url) and not url.endswith(('.py', '.js', '.css', '.html', '.txt', '.json', '.xml')):
                urls.append(url)
    
    return list(set(urls))

def check_token_send(message):

    token_patterns = [
        r'[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}',
        r'[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{38}',
        r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}',
    ]
    
    for pattern in token_patterns:
        if re.search(pattern, message.content):
            return "トークンの送信が検出されました"
    return None

def check_invite_links(message):

    invite_patterns = [
        r'(?:https?://)?(?:www\.)?discord\.gg/([a-zA-Z0-9\-_]+)',
        r'(?:https?://)?(?:www\.)?discord\.com/invite/([a-zA-Z0-9\-_]+)',
        r'(?:https?://)?(?:www\.)?discordapp\.com/invite/([a-zA-Z0-9\-_]+)',
        r'(?:https?://)?(?:www\.)?discord\.io/([a-zA-Z0-9\-_]+)',
        r'(?:https?://)?(?:www\.)?discord\.me/([a-zA-Z0-9\-_]+)',
        r'(?:https?://)?(?:www\.)?discord\.li/([a-zA-Z0-9\-_]+)',
        r'(?:^|\s)discord\.gg/([a-zA-Z0-9\-_]+)',
        r'(?:^|\s)discord\.com/invite/([a-zA-Z0-9\-_]+)',
    ]
    
    for pattern in invite_patterns:
        match = re.search(pattern, message.content, re.IGNORECASE)
        if match:
            allowed_channels = invite_whitelist_channels.get(message.guild.id, set())
            if message.channel.id not in allowed_channels:
                return "許可されていないチャンネルでの招待リンク送信が検出されました"
            break
    
    return None

def check_shortlinks(message):

    urls = extract_urls_from_message(message.content)
    
    for url in urls:
        domain = url.lower()
        for prefix in ['https://', 'http://', 'www.']:
            if domain.startswith(prefix):
                domain = domain[len(prefix):]
        domain = domain.split('/')[0]
        domain = domain.split(':')[0]
        
        for shortlink_domain in SHORTLINK_DOMAINS:
            if domain == shortlink_domain or domain.endswith('.' + shortlink_domain):
                return f"短縮リンクが検出されました ({domain})"
    return None

def check_malware_links(message):

    urls = extract_urls_from_message(message.content)
    
    for url in urls:

        check_url = url
        if not check_url.startswith(('http://', 'https://')):
            check_url = 'http://' + check_url
        
        if check_url_with_filter(check_url):
            return f"マルウェアリンクが検出されました ({url})"
    return None

def check_spam(message):

    user_id = message.author.id
    current_time = datetime.now()
    
    user_message_counts[user_id] = [
        (content, time) for content, time in user_message_counts[user_id]
        if current_time - time < timedelta(seconds=10)
    ]
    
    same_messages = sum(1 for content, _ in user_message_counts[user_id] 
                       if content == message.content)
    
    if same_messages >= 3:
        return "スパムが検出されました（同一メッセージの連投）"
    
    user_message_counts[user_id].append((message.content, current_time))
    return None

def check_flood(message):

    user_id = message.author.id
    current_time = datetime.now()
    
    recent_messages = [t for t in user_message_times[user_id] 
                      if current_time - t < timedelta(seconds=5)]
    
    if len(recent_messages) >= 5:
        return "フラッドが検出されました（短時間での大量メッセージ）"
    
    user_message_times[user_id].append(current_time)
    if len(user_message_times[user_id]) > 10:
        user_message_times[user_id] = user_message_times[user_id][-10:]
    
    return None

def check_emoji_spam(message):

    custom_emoji = len(re.findall(r'<a?:[a-zA-Z0-9_]+:[0-9]+>', message.content))
    unicode_emoji = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF'
                                   r'\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF'
                                   r'\U00002702-\U000027B0\U000024C2-\U0001F251]', message.content))
    
    total_emoji = custom_emoji + unicode_emoji
    if total_emoji > 0 and total_emoji / max(len(message.content.split()), 1) >= 0.5:
        return "絵文字スパムが検出されました"
    return None

def check_spoiler_spam(message):

    spoiler_count = message.content.count('||')
    if spoiler_count >= 10:
        return "スポイラースパムが検出されました"
    return None

def check_markdown_spam(message):

    markdown_patterns = [
        r'#{1,6}\s',
    ]
    
    markdown_count = 0
    for pattern in markdown_patterns:
        markdown_count += len(re.findall(pattern, message.content))
    
    if markdown_count >= 5:
        return "マークダウンスパムが検出されました"
    return None
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message('❌ このコマンドを実行する権限がありません', ephemeral=True)
    else:
        await interaction.response.send_message(f'❌ エラーが発生しました: {error}', ephemeral=True)

if __name__ == "__main__":
    bot.run(TOKEN)

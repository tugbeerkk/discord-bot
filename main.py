import discord
from discord.ext import commands
from model import decect_bird
from molov import detect_objects
from matabase import setup_database, add_user, get_user_balance,change_balance,UserAlreadyExistsError,update_balance
from mlackjack import Blackjack
import random

intents = discord.Intents.default()
intents.message_content = True

game = None
bjc = None

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    setup_database()


@bot.command()
async def yt(ctx, amount: str):  # `amount` parametresi, kullanıcı tarafından girilen sayıyı alacak.
    try:
        user_id = ctx.author.id
        amount1 = -int(amount.strip())
        update_balance(user_id, amount1)
        sayi = random.randint(1,2)
        if sayi == 1  :   
            await ctx.send(f"Maalesef {amount1} tl kaybettin ")
        elif sayi == 2 :
            amount2 = int(amount.strip()) * 2
            update_balance(user_id,amount2)
            await ctx.send(f"Tebrikler {amount2} tl kazandın ")
    except ValueError:
        await ctx.send("Geçersiz bir sayı girdiniz. Örnek kullanım: `.yt 100`")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {e}")

@bot.command()
async def gh(ctx, amount: str):  # `amount` parametresi, kullanıcı tarafından girilen sayıyı alacak.
    user_id = ctx.author.id
    amount1 = int(amount.strip())
    update_balance(user_id, amount1)

@bot.command()
async def register(ctx):
    user_id = ctx.author.id
    username = ctx.author.name
    try:
        add_user(user_id, username)
        await ctx.send(f"{username} başarıyla kaydedildi!")
    except UserAlreadyExistsError:
        await ctx.send(f"{username} zaten kayıtlı!")

@bot.command()
async def balance(ctx):
    user_id = ctx.author.id
    balance = get_user_balance(user_id)
    await ctx.send(f"{ctx.author.name}, bakiyeniz: {balance} tl.")

@bot.command()
async def daily(ctx):
    user_id = ctx.author.id # Komutu çalıştıran kullanıcının ID'sini al
    amount = random.randint(500,1000)
    try:
        change_balance(user_id, amount)
        ctx.send(f"Günlük bakiye hediyeniz:{amount}")
    except ValueError as e:
        await ctx.send(f"İşlem başarısız! Hata: {e}")  

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            filename = attachment.filename
            urlname = attachment.url
            await attachment.save(f"{attachment.filename}")
            await ctx.send(f"Fotoğraf başarıyla kaydedildi {attachment.filename} ")
            deger = (decect_bird("keras_model.h5","labels.txt",attachment.filename))
            if deger <= 0.5:
                await ctx.send("Görseli algılayamadım")
            elif deger > 0.5:
                await ctx.send(deger)
    else:
        await ctx.send("Bir fotoğraf eklemelisiniz")

@bot.command()
async def detect(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            filename = attachment.filename
            urlname = attachment.url
            await attachment.save(f"{attachment.filename}")
            await ctx.send(f"Fotoğraf başarıyla kaydedildi {attachment.filename} ")
            
            detections, output_image_path = detect_objects(attachment.filename)
            if detections:
                detection_text = "\n".join(
                    [f"{d['name']} - {d['probability']:.2f}%" for d in detections]
                )
                await ctx.send(f"Algılanan nesneler ve doğruluk oranları:\n{detection_text}")

                with open(output_image_path, "rb") as img_file:
                    await ctx.send("İşlenen görsel:", file=discord.File(img_file))
            else:
                await ctx.send("Hiçbir nesne algılanamadı.")
    else:
        await ctx.send("Henüz bir dosya yüklenmedi.")

@bot.command()
async def bj(ctx, amount: str):
    try:
        global game
        game = Blackjack()
        player_hand, dealer_hand = game.start_game()
        user_id = ctx.author.id
        amount1 = -int(amount)
        global bjc
        bjc = int(amount)*2
        update_balance(user_id, amount1)
        
        await ctx.send(f"Your hand: {player_hand}, Total: {game.calculate_hand(player_hand)}")
        await ctx.send(f"Dealer shows: {dealer_hand[0]}")
    except ValueError:
        await ctx.send("Geçersiz bir sayı girdiniz. Örnek kullanım: `.bj 100`")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {e}")
@bot.command()
async def hit(ctx):
    try:
        user_id = ctx.author.id
        global bjc
        global game
        if not game:
            await ctx.send("Start a new game with !blackjack first.")
            return

        card = game.player_hit()
        total = game.calculate_hand(game.player_hand)
        await ctx.send(f"You drew {card}. Your hand: {game.player_hand}, Total: {total}")

        if total > 21:
            await ctx.send("You busted! Dealer wins.")
            update_balance(user_id, bjc)
            game = None
            bjc  = None
        if total == 21:
            await ctx.send("Congratulations! You hit 21 and won!")
            game = None
            bjc  = None
            return
        
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {e}")

@bot.command()
async def stand(ctx):
    try:    
        user_id = ctx.author.id
        global bjc
        global game
        if not game:
            await ctx.send("Start a new game with !blackjack first.")
            return

        game.dealer_play()
        dealer_total = game.calculate_hand(game.dealer_hand)
        await ctx.send(f"Dealer's hand: {game.dealer_hand}, Total: {dealer_total}")

        result_message, result_code = game.get_winner()
        await ctx.send(result_message)
        if result_code==0:
            update_balance(user_id, bjc/2)
        elif result_code==1:
            update_balance(user_id, bjc)
        elif result_code==4:
            update_balance(user_id, bjc)
        else:
            None

        game = None
        bjc = None
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {e}")
bot.run(bot token)

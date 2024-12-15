$BotToken = "7860835594:AAFnmHlf1AVFKQ6fKGr0UaYgwhNj-J95cZ0"
$ChatId = "526626246"
$Message = "task schedule!"
$Url = "https://api.telegram.org/bot$BotToken/sendMessage"
$Payload = @{
    chat_id = $ChatId
    text = $Message
}
$response = Invoke-RestMethod -Uri $Url -Method Post -ContentType "application/json" -Body ($Payload | ConvertTo-Json -Depth 10)

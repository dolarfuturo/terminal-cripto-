// @version=5
indicator("Eixo Alpha Vision - BTC", overlay=true)

// Configuração de Horário (Brasília UTC-3)
sessao_ny = (hour == 11 and minute >= 30) or (hour > 11 and hour < 18)

var float max_d = na
var float min_d = na
var float eixo = na

// Captura de dados
if sessao_ny
    max_d := not sessao_ny[1] ? high : math.max(high, max_d)
    min_d := not sessao_ny[1] ? low : math.min(low, min_d)

// Trava o Eixo às 18:00
if hour == 18 and minute == 0
    eixo := (max_d + min_d) / 2

// Alvos Baseados no Eixo Travado
a_04   = eixo * 1.004
a_061  = eixo * 1.0061
a_122  = eixo * 1.0122

b_04   = eixo * 0.996
b_061  = eixo * 0.9939
b_122  = eixo * 0.9878

// Plotagem - Só aparece se o Eixo existir
plot(eixo, "EIXO MESTRE", color=color.yellow, linewidth=3, style=plot.style_linebr)

// Alvos de Alta (Verdes)
plot(eixo > 0 ? a_04 : na,  "0.4%",  color=color.new(color.gray, 50))
plot(eixo > 0 ? a_061 : na, "0.61%", color=color.new(color.green, 50))
plot(eixo > 0 ? a_122 : na, "1.22%", color=color.green, linewidth=2)

// Alvos de Baixa (Vermelhos)
plot(eixo > 0 ? b_04 : na,  "0.4%",  color=color.new(color.gray, 50))
plot(eixo > 0 ? b_061 : na, "0.61%", color=color.new(color.red, 50))
plot(eixo > 0 ? b_122 : na, "1.22%", color=color.red, linewidth=2)

import tkinter as tk

CINZENTO_CLARO = '#F5F5F5'
BRANCO = '#FFFFFF'
BRANCO_SUJO = '#F8FAFF'
AZUL_CLARO = '#CCEDFF'
COR_LABEL = '#25265E'

ESTILO_FONTE_PEQUENO = ('Arial', 16)
ESTILO_FONTE_GRANDE = ('Arial', 40, 'bold')
ESTILO_FONTE_NUMEROS = ('Arial', 24, 'bold')
ESTILO_FONTE_DEFAULT = ('Arial', 20)


class Calculadora:

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.geometry('375x667')
        self.janela.resizable(0, 0)
        self.janela.title('Calculadora')

        self.expressao_total = ''
        self.expressao_atual = ''
        self.frame_display = self.criar_frame_display()
        self.frame_botoes = self.criar_frame_botoes()
        self.label_total, self.label = self.criar_display_labels()

        self.numeros = {
            7 : (1, 1), 8 : (1, 2), 9 : (1, 3),
            4 : (2, 1), 5 : (2, 2), 6 : (2, 3),
            1 : (3, 1), 2 : (3, 2), 3 : (3, 3),
            '.' : (4, 1), 0 : (4, 2)
        }

        self.operacoes = {'/' : '\u00F7', '*' : '\u00D7', '-' : '-', '+' : '+'}

        self.frame_botoes.rowconfigure(0, weight = 1)

        for x in range(1, 5):
            self.frame_botoes.rowconfigure(x, weight = 1)
            self.frame_botoes.columnconfigure(x, weight = 1)

        self.criar_botoes_numeros()
        self.criar_botoes_operacoes()
        self.criar_botoes_especiais()
        self.bind_teclas()
    
    def bind_teclas(self):
        self.janela.bind('<Return>', lambda evento: self.avaliar())
        for key in self.numeros:
            self.janela.bind(str(key), lambda evento, numero = key: self.adicionar_a_expressao(numero))
        for key in self.operacoes:
            self.janela.bind(key, lambda evento, operador = key: self.append_operador(operador))

    def criar_botoes_especiais(self):
        self.criar_botao_clear()
        self.criar_botao_igual()
        self.criar_botao_quadrado()
        self.criar_botao_raiz_quadrada()
    
    def criar_display_labels(self):
        label_total = tk.Label(self.frame_display, text = self.expressao_total, anchor = tk.E, bg = CINZENTO_CLARO, fg = COR_LABEL, padx = 24, font = ESTILO_FONTE_PEQUENO)
        label_total.pack(expand = True, fill = 'both')

        label = tk.Label(self.frame_display, text = self.expressao_atual, anchor = tk.E, bg = CINZENTO_CLARO, fg = COR_LABEL, padx = 24, font = ESTILO_FONTE_GRANDE)
        label.pack(expand = True, fill = 'both')

        return label_total, label

    def criar_frame_display(self):
        frame = tk.Frame(self.janela, height = 221, bg = CINZENTO_CLARO)
        frame.pack(expand = True, fill = 'both')

        return frame
    
    def criar_frame_botoes(self):
        frame = tk.Frame(self.janela)
        frame.pack(expand = True, fill = 'both')

        return frame
    
    def criar_botoes_numeros(self):
        for numero, valor_grid in self.numeros.items():
            botao = tk.Button(self.frame_botoes, text = str(numero), bg = BRANCO, fg = COR_LABEL, font = ESTILO_FONTE_NUMEROS, borderwidth = 0,
                              command = lambda x = numero: self.adicionar_a_expressao(x))
            botao.grid(row = valor_grid[0], column = valor_grid[1], sticky = tk.NSEW)

    def append_operador(self, operador):
        self.expressao_atual += operador
        self.expressao_total += self.expressao_atual
        self.expressao_atual = ''
        self.atualizar_label_total()
        self.atualizar_label()

    def criar_botoes_operacoes(self):
        i = 0
        for operador, simbolo in self.operacoes.items():
            botao = tk.Button(self.frame_botoes, text = simbolo, bg = BRANCO_SUJO, fg = COR_LABEL, font = ESTILO_FONTE_DEFAULT, borderwidth = 0,
                              command = lambda x = operador: self.append_operador(x))
            botao.grid(row = i, column = 4, sticky = tk.NSEW)
            i += 1
    
    def clear(self):
        self.expressao_atual = ''
        self.expressao_total = ''
        self.atualizar_label()
        self.atualizar_label_total()

    def criar_botao_clear(self):
        botao = tk.Button(self.frame_botoes, text = 'C', bg = BRANCO_SUJO, fg = COR_LABEL, font = ESTILO_FONTE_DEFAULT, borderwidth = 0,
                          command = self.clear)
        botao.grid(row = 0, column = 1, sticky = tk.NSEW)

    def quadrado(self):
        self.expressao_atual = str(eval(f'{self.expressao_atual}**2'))
        self.atualizar_label()

    def criar_botao_quadrado(self):
        botao = tk.Button(self.frame_botoes, text = 'x\u00b2', bg = BRANCO_SUJO, fg = COR_LABEL, font = ESTILO_FONTE_DEFAULT, borderwidth = 0,
                          command = self.quadrado)
        botao.grid(row = 0, column = 2, sticky = tk.NSEW)

    def raiz_quadrada(self):
        self.expressao_atual = str(eval(f'{self.expressao_atual}**0.5'))
        self.atualizar_label()

    def criar_botao_raiz_quadrada(self):
        botao = tk.Button(self.frame_botoes, text = '\u221ax', bg = BRANCO_SUJO, fg = COR_LABEL, font = ESTILO_FONTE_DEFAULT, borderwidth = 0,
                          command = self.raiz_quadrada)
        botao.grid(row = 0, column = 3, sticky = tk.NSEW)

    def avaliar(self):
        self.expressao_total += self.expressao_atual
        self.atualizar_label_total()
        try:
            self.expressao_atual = str(eval(self.expressao_total))
            self.expressao_total = ''
        except Exception as e:
            self.expressao_atual = 'Erro'
        finally:
            self.atualizar_label()

    def criar_botao_igual(self):
        botao = tk.Button(self.frame_botoes, text = '=', bg = AZUL_CLARO, fg = COR_LABEL, font = ESTILO_FONTE_DEFAULT, borderwidth = 0,
                          command = self.avaliar)
        botao.grid(row = 4, column = 3, columnspan = 2, sticky = tk.NSEW)

    def adicionar_a_expressao(self, valor):
        self.expressao_atual += str(valor)
        self.atualizar_label()

    def atualizar_label_total(self):
        expressao = self.expressao_total
        for operador, simbolo in self.operacoes.items():
            expressao = expressao.replace(operador, f' {simbolo} ')
        self.label_total.config(text = expressao)

    def atualizar_label(self):
        self.label.config(text = self.expressao_atual[:11])

    def correr(self):
        self.janela.mainloop()
    
if __name__ == '__main__':
    calc = Calculadora()
    calc.correr()
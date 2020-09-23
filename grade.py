import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle
import os.path
import disciplina as disc
"""----------------------------------------------------------"""
# Possíveis erros que vão ser tratados por expections
class InvalidYear(Exception):
    pass

class DisciplinaAlreadyExists(Exception):
    pass

class InvalidCode(Exception):
    pass

class informationAlreadyExists(Exception):
    pass

class EmptyField(Exception):
    pass
"""----------------------------------------------------------"""
# Classe importante GRADE
class Grade:
    # Método construtor da grade
    def __init__(self, codigoGrade, yearGrade, semesterGrade):
        self.__codigoGrade = codigoGrade
        self.__yearGrade = yearGrade
        self.__semesterGrade = semesterGrade
        # Lista com as disciplinas da grade
        self.__disciplinasGradeList = []

    # Métodos Getters
    def getDisciplinasGradeList(self):
        return self.__disciplinasGradeList

    def getCodigoGrade(self):
        return self.__codigoGrade

    def getYearGrade(self):
        return self.__yearGrade

    def getSemesterGrade(self):
        return self.__semesterGrade

    # Método para adicionar disciplina
    def addDisciplina(self, disciplina):
        self.__disciplinasGradeList.append(disciplina)
"""----------------------------------------------------------"""
# Limite da tela de inserção da grade
class InsereGradeView(tk.Toplevel):
    # Método construtor
    def __init__(self, control, disciplinasList):
        tk.Toplevel.__init__(self)
        # Tamanho da janela
        self.geometry("400x400")
        # Cria o título
        self.title('CADASTRO DE GRADE/ INSIRA')
        # Controle
        self.control = control
        # Criar as partes necessárias de pegar a código da grade
        self.frameCodigoGrade = tk.Frame(self)
        self.frameCodigoGrade.pack()
        self.labelCodigoGrade = tk.Label(self.frameCodigoGrade, text='CÓDIGO:')
        self.labelCodigoGrade.pack(side='left')
        self.inputCodigoGrade = tk.Entry(self.frameCodigoGrade, width=20)
        self.inputCodigoGrade.pack(side='left')
        # Criar as partes necessárias de pegar o ano da grade
        self.frameYearGrade = tk.Frame(self)
        self.frameYearGrade.pack()
        self.labelYearGrade = tk.Label(self.frameYearGrade, text='ANO:')
        self.labelYearGrade.pack(side='left')
        self.inputYearGrade = tk.Entry(self.frameYearGrade, width=20)
        self.inputYearGrade.pack(side='left')
        # Criar as partes necessárias de pegar o semestre da grade
        self.frameSemesterGrade = tk.Frame(self)
        self.frameSemesterGrade.pack()
        self.labelSemesterGrade = tk.Label(self.frameSemesterGrade, text='SEMESTRE: ')
        self.labelSemesterGrade.pack(side='left')
        self.chooseCombo = tk.StringVar()
        self.comboboxSemesterGrade = ttk.Combobox(self.frameSemesterGrade, width=20, textvariable=self.chooseCombo)
        self.comboboxSemesterGrade.pack(side='left')
        # Lista para o combobox que faz aparecer essas opções
        self.semestresList = ['1', '2']
        self.comboboxSemesterGrade['values'] = self.semestresList
        # Criar as partes necessárias das disciplinas na grade
        self.frameDisciplinaGrade = tk.Frame(self)
        self.frameDisciplinaGrade.pack()
        self.labelDisciplinaGrade = tk.Label(
            self.frameDisciplinaGrade, text='\n\nDISCIPLINAS:')
        self.labelDisciplinaGrade.pack()
        self.chooseComboDisciplina = tk.StringVar()
        self.comboboxDisciplina = ttk.Combobox(self.frameDisciplinaGrade, width=20, textvariable=self.chooseComboDisciplina)
        self.comboboxDisciplina.pack(side='top')

        # cria uma lista para os código da disciplina
        codigosDisciplinas = []
        for disc in disciplinasList:
            codigosDisciplinas.append(disc.getCodigoDisciplina())
        # Adiciona os valores da lista no combobox
        self.comboboxDisciplina['values'] = codigosDisciplinas

        # Botões
        # Criar o frame dos botões
        self.frameButton = tk.Frame(self)
        self.frameButton.pack()
        # Botão para inserir disciplina
        self.buttonInsere = tk.Button(self.frameDisciplinaGrade, text='INSERIR DISCIPLINA')
        self.buttonInsere.pack(side='top')
        self.buttonInsere.bind("<Button>", control.insereDisciplina)
        # Botão para criar grade
        self.buttonCria = tk.Button(self.frameButton, text='CRIAR GRADE', font=('Negrito', 11))
        self.buttonCria.pack(side='left')
        self.buttonCria.bind("<Button>", control.createGrade)
        # Botão para limpar os campos já preenchidos pelo usuário
        self.buttonClear = tk.Button(self.frameButton, text='LIMPAR', font=('Negrito', 11))
        self.buttonClear.pack(side='left')
        self.buttonClear.bind("<Button>", control.clearHandler)
        # Botão para sair após criar a grade
        self.buttonConcluido = tk.Button(self.frameButton, text='FECHAR', font=('Negrito', 11))
        self.buttonConcluido.pack(side='left')
        self.buttonConcluido.bind("<Button>", control.concluiHandler)

    # Método para mostrar mensagens de aviso para o usuário
    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)
"""----------------------------------------------------------"""
# Limite para mostrar as informações que já foram cadastradas
class MostraGradesView():
    def __init__(self, str):
        messagebox.showinfo('LISTA DE GRADES CADASTRADAS', str)
"""----------------------------------------------------------"""
# Classe controladora da grade
class CtrlGrade():
    # Método construtor
    def __init__(self, mainControl):
        # Passando como parâmetro controlador principal
        self.ctrlMain = mainControl
        # ---Ler as informações dos arquivos que foram salvos ---
        if not os.path.isfile("grades.pickle"):
            self.gradesList = []
        else:
            with open("grades.pickle", "rb") as f:
                self.gradesList = pickle.load(f)
        # Lista com disciplinas
        self.disciplinaGradeList = []

    # Método para inserir a grade
    def insereGrade(self):
        # Lista com apenas a lista de disciplinas
        disciplinasList = self.ctrlMain.ctrlDisciplina.getDisciplinasList()
        # Chama o limite da inserção da grade, passando como parâmetro a lista de disciplinas
        self.limiteIns = InsereGradeView(self, disciplinasList)

    # Método para inserirs as disciplinas na grade
    def insereDisciplina(self, event):
        try:
            # Verificando se tem algum campo de preenchimento vazio
            if len(self.limiteIns.inputYearGrade.get()) == 0 or len(self.limiteIns.chooseCombo.get()) == 0 or len(self.limiteIns.inputCodigoGrade.get()) == 0:
                raise EmptyField()
            # Verifica se o código da grade é inválido
            if len(self.limiteIns.inputCodigoGrade.get()) != 2 or not self.limiteIns.inputCodigoGrade.get().isdigit():
                raise InvalidCode()
            # Verificando se tem o ano está inválido. Precisa estar entre 2012 e 2040
            if int(self.limiteIns.inputYearGrade.get()) > 2040 or int(self.limiteIns.inputYearGrade.get()) < 2012 or not self.limiteIns.inputYearGrade.get().isdigit():
                raise InvalidYear()
        # Mostra mensagem avisando o usuário sobre o erro
        except EmptyField:
            self.limiteIns.mostraJanela('AVISO!', 'PREENCHA TODOS OS CAMPOS')
        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidCode:
            self.limiteIns.mostraJanela("AVISO!", "CÓDIGO INVÁLIDO! EXEMPLO: 01")
        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidYear:
            self.limiteIns.mostraJanela('AVISO!', 'ANO INVÁLIDO! PRECISA ESTAR ENTRE 2012 A 2040')
        # Caso não tenha erros das exeptions acima
        else:
            # A disciplina selecionada é escolhida
            currentDisc = self.limiteIns.comboboxDisciplina.get()
            # É buscado o objeto da disciplina que estava selecionada
            objDisciplina = self.ctrlMain.ctrlDisciplina.getDisciplinaObj(currentDisc)
            try:
                # Verifica se a disciplina já existe
                for disciplina in self.disciplinaGradeList:
                    if objDisciplina.getCodigoDisciplina() == disciplina.getCodigoDisciplina():
                        raise DisciplinaAlreadyExists()
            # Mostra mensagem avisando o usuário sobre o erro
            except DisciplinaAlreadyExists:
                self.limiteIns.mostraJanela("AVISO!", "DISCIPLINA JÁ INSERIDA NA GRADE")
            # Caso não tenha erro da exeption acima
            else:
                # Adiciona-se o objeto dessa disciplina na lista de disciplinas
                self.disciplinaGradeList.append(objDisciplina)
                self.limiteIns.mostraJanela('CONGRULATIONS!', 'DISCIPLINA CADASTRADA')

    # Método para criar a grade
    def createGrade(self, event):
        try:
            # Verificando se tem algum campo de preenchimento vazio
            if len(self.limiteIns.inputYearGrade.get()) == 0 or len(self.limiteIns.chooseCombo.get()) == 0 or len(self.limiteIns.inputCodigoGrade.get()) == 0:
                raise EmptyField()
            # Verifica se o código da grade é inválido
            if len(self.limiteIns.inputCodigoGrade.get()) != 2 or not self.limiteIns.inputCodigoGrade.get().isdigit():
                raise InvalidCode()
            # Verificando se tem o ano está inválido. Precisa estar entre 2012 e 2040
            if int(self.limiteIns.inputYearGrade.get()) > 2040 or int(self.limiteIns.inputYearGrade.get()) < 2012 or not self.limiteIns.inputYearGrade.get().isdigit():
                raise InvalidYear()
        # Mostra mensagem avisando o usuário sobre o erro
        except EmptyField:
            self.limiteIns.mostraJanela('AVISO', 'PREENCHA TODOS OS CAMPOS')
        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidCode:
            self.limiteIns.mostraJanela("AVISO", "CÓDIGO INVÁLIDO! EXEMPLO: 01")
        # Mostra mensagem avisando o usuário sobre o erro
        except InvalidYear:
            self.limiteIns.mostraJanela('AVISO', 'ANO INVÁLIDO! PRECISA ESTAR ENTRE 2012 A 2040')
        # Caso não tenha erros das exeptions acima
        else:
            codigoCurso = self.limiteIns.inputCodigoGrade.get()
            year = self.limiteIns.inputYearGrade.get()
            semester = self.limiteIns.chooseCombo.get()
            # Instancia a grade
            grade = Grade(codigoCurso, year, semester)
            # Adiciona as disciplina na grade
            for disc in self.disciplinaGradeList:
                grade.addDisciplina(disc)
            try:
                # Verificando se já o existe o código da grade
                for gra in self.gradesList:
                    if gra.getCodigoGrade() == grade.getCodigoGrade():
                        raise informationAlreadyExists()
            # Mostra mensagem avisando o usuário sobre o erro
            except informationAlreadyExists:
                self.limiteIns.mostraJanela('AVISO!', 'CÓDIGO DA GRADE JÁ EXISTE')
            # Caso não tenha erro da exeption acima
            else:
                # Adiciona a grade instanciada na lista de grades
                self.gradesList.append(grade)
                self.limiteIns.mostraJanela('CONGRULATIONS!', 'GRADE CADASTRADA')

    # Método para mostrar as grades
    def mostraGrades(self):
        str = ''
        if len(self.gradesList) != 0:
            for gra in self.gradesList:
                str += '~~ GRADE ~~\n'
                str += 'CÓDIGO ~~ ANO/SEMESTRE DO ANO\n'
                str += f'{gra.getCodigoGrade()} -- {gra.getYearGrade()}.{gra.getSemesterGrade()}'
                str += '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
                str += f'DISCIPLINAS DA GRADE {gra.getCodigoGrade()}:\n'
                for disc in gra.getDisciplinasGradeList():
                    str += "CÓDIGO ~~ NOME ~~ CARGA TOTAL\n"
                    str += f'{disc.getCodigoDisciplina()} -- {disc.getNomeDisciplina()} -- {disc.getCargaHoraria()}'
                    str += '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
        else:
            str += 'Não existem grades cadastradas!'
        self.limiteMost = MostraGradesView(str)

    # Método getter para pegar a lista de grades
    def getGradesList(self):
        return self.gradesList

    # Método getter para pegar o objeto grade
    def getGradeObj(self, codigoGrade):
        # Declara um objeto vazio
        objGrade = None
        # Se o código da grade passado como parâmetro é igual então ele retorna o objeto grade inteiro
        for gra in self.gradesList:
            if codigoGrade == gra.getCodigoGrade():
                objGrade = gra
        return objGrade

    def getGradeObjByCurso(self, cursoAluno):
        temp = self.ctrlMain.ctrlCurso.getCursosList()
        # Declara um objeto vazio
        objGrade = None
        # Se a curso passado como parâmetro é igual então ele retorna o objeto grade inteiro para passar para o aluno
        for curso in temp:
            if cursoAluno.getCodigoCurso() == curso.getCodigoCurso():
                objGrade = cursoAluno.getGrade()
        return objGrade

    # Método para limpar os campos de preenchimento que foram preenchidos
    def clearHandler(self, event):
        self.limiteIns.inputYearGrade.delete(0, len(self.limiteIns.inputYearGrade.get()))
        self.limiteIns.inputCodigoGrade.delete(0, len(self.limiteIns.inputCodigoGrade.get()))
        self.limiteIns.comboboxSemesterGrade.delete(0, len(self.limiteIns.comboboxSemesterGrade.get()))

    # Método para destruir a tela e sair
    def concluiHandler(self, event):
        self.limiteIns.destroy()

    # Método para salvar todas as informações que foram registradas
    def saveGrades(self):
        if len(self.gradesList) != 0:
            with open("grades.pickle", "wb") as f:
                pickle.dump(self.gradesList, f)
"""----------------------------------------------------------"""
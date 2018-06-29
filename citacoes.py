from time import sleep
from selenium import webdriver


def main():

    class Theend():
         """Classe para acessar o site Theend
         e retorna os titulos utilizados no Mapeamento sistemático """

        def __init__(self, driver):
            self.driver = driver
            self.url = 'https://easii.ufpi.br/theend/home/login'

        def _theend(self):
            """Acessa o site Theend : https://easii.ufpi.br/theend/ """
            self.driver.get(self.url)

        def _login(self):
            """Loga no site Theend"""
            login = self.driver.find_element_by_id('login')
            # insira o login na função login.send.keys()
            login.send_keys()
            password = self.driver.find_element_by_name('password')
            # insira a senha na função passwordsend.keys()
            password.send_keys()
            botao = self.driver.find_element_by_id('submit')  # pega o botao
            botao.click()  # clica no botao

        def _quantidade_paginas(self):
            """Calcula a quantidade de paginas necessários
            pra pecorrer todos os artigos resultante da busca"""
            total_artigos = self._total_artigos()
            if total_artigos <= 10:
                return 1
            elif total_artigos <= 20:
                quantidade_elementos = self.driver.find_element_by_name(
                    'DataTables_Table_0_length')
                quantidade_elementos.send_keys('20')
                return 1
            elif total_artigos <= 25:
                quantidade_elementos = self.driver.find_element_by_name(
                    'DataTables_Table_0_length')
                quantidade_elementos.send_keys('25')
                return 1
            elif total_artigos <= 50:
                quantidade_elementos = self.driver.find_element_by_name(
                    'DataTables_Table_0_length')
                quantidade_elementos.send_keys('50')
                return 1
            elif total_artigos <= 100:
                quantidade_elementos = self.driver.find_element_by_name(
                    'DataTables_Table_0_length')
                quantidade_elementos.send_keys('100')
                return 1
            else:
                qnt_paginas = total_artigos / 100
                if type(qnt_paginas) == float:
                    qnt_paginas = int(qnt_paginas) + 1
                    quantidade_elementos = self.driver.find_element_by_name(
                        'DataTables_Table_0_length')
                    quantidade_elementos.send_keys('100')
                return qnt_paginas

        def _total_artigos(self):
            """pega o total de artigos usados no Mapeamento Sistemático """
            total_artigos = self.driver.find_element_by_class_name(
                'dataTables_info').text
            total_artigos = total_artigos.split(" ")[-2]
            return int(total_artigos)

        def _passa_pagina(self, page):
            """Passa a pagina no site Theend"""
            pagination = self.driver.find_element_by_class_name('pagination')
            pagina = pagination.find_elements_by_tag_name('li')[page]
            link = pagina.find_element_by_tag_name('a')
            link.click()

        def principal(self):
            """Função principal"""
            self._theend()
            self._login()
            lista = self.driver.find_element_by_class_name('table')
            lista.click()
            mapeamento = self.driver.find_element_by_class_name('odd')
            mapeamento = mapeamento.find_element_by_tag_name('a')
            mapeamento.click()
            self.driver.switch_to_alert().accept()  # alerta.
            self.driver.switch_to_alert().accept()  # outro alerta.
            extracao = self.driver.find_elements_by_class_name('col-md-12')
            extracao = extracao[2].find_element_by_tag_name('a')
            extracao.click()
            paginas = self._quantidade_paginas()
            titulos_artigos = []
            for pagina in range(paginas):
                artigos = self.driver.find_elements_by_class_name('readArticle')
                artigos = [artigos[i].text for i in range(len(artigos))]
                titulos_artigos.append(artigos)
                self._passa_pagina(pagina + 2)
            return titulos_artigos

    class Scopus:
        """ inicializa o Scopus com as URL's do site utilizado na captura de dados."""

        def __init__(self, driver):
            self.driver = driver
            self.url_scopus = 'https://www-scopus.ez17.periodicos.capes.gov.br/search/form.uri?display=basic'
            self.citacoes = []
            self.nomes_artigos = []

        def _scopus(self):
            """
            Acessa o Site Scopus :
            https://www-scopus.ez17.periodicos.capes.gov.br/search/form.uri?display=basic
            com proxy de uma Universidade
            """
            self.driver.get(self.url_scopus)

        def _pega_qnt_artigos(self):
            """
            captura a quantidade de artigos resutantes na busca do site Scopus e transforma o a string da quantidade
            em inteiro
            """
            try:
                qnt_artigos_encontrados = int(
                    self.driver.find_element_by_class_name('resultsCount').text)
            except:
                """
                se o resultado da quantidade encontrada for um float com muitos elementos
                 tira-se a virgula do float e converte pra inteiro"""
                qnt_artigos_encontrados = int(
                    (self.driver.find_element_by_class_name('resultsCount').text).replace(',', ''))
            return qnt_artigos_encontrados

        def _muda_tamanho_pagina(self):
            """ altera a quantidade de artigos exibidos por pagina baseado na quantidade de artigos encontrados na busca"""
            qnt_artigos_encontrados = self._pega_qnt_artigos()
            if qnt_artigos_encontrados <= 20:
                # se quantidade de artigos encontrados for menor ou igual a 20 então 1
                # pagina com 20 elementos resolve.
                return 1
            if qnt_artigos_encontrados <= 50:
                # se quantidade de artigos encontrados for menor ou igual a 50 então 1
                # pagina com 50 elementos resolve
                num_pages = self.driver.find_elements_by_class_name(
                    'extraSmallSelect')
                num_pages[1].send_keys('50')
                return 1
            if qnt_artigos_encontrados <= 100:
                # se quantidade de artigos encontrados for menor ou igual a 100 então 1
                # pagina com 100 elementos resolve.
                num_pages = self.driver.find_elements_by_class_name(
                    'extraSmallSelect')
                num_pages[1].send_keys('100')
                return 1
            if qnt_artigos_encontrados <= 200:
                # se quantidade de artigos encontrados for menor ou igual a 200 então 1
                # pagina com 200 elementos resolve.
                num_pages = self.driver.find_elements_by_class_name(
                    'extraSmallSelect')
                num_pages[1].send_keys('200')
                return 1
            else:
                # se quantidade de artigos encontrados ultrapassar o numero maximos de elemntos que uma pagina pode exibir
                # calcula-se o numero de paginas, com 200 elementos, necessário para
                # percorrer todos os artigos
                qnt_paginas = qnt_artigos_encontrados / 200
                if type(qnt_paginas) == float:
                    qnt_paginas = int(qnt_paginas) + 1
                num_pages = self.driver.find_elements_by_class_name(
                    'extraSmallSelect')
                num_pages[1].send_keys('200')
                return qnt_paginas

        def _passa_pagina(self, page):
            """Passa a pagina no site Scopus"""
            pages = self.driver.find_element_by_class_name('pagination')
            pages.driver.find_elements_by_tag_name('li')[page].click()

        def _procura_e_compara_artigo(self, nome):
            """busca pelo titulo na pagina do Scopus e comparar os titulos"""
            qnt_paginas = self._muda_tamanho_pagina()
            for pagina in range(qnt_paginas):
                tabela_artigos = self.driver.find_element_by_id('srchResultsList')
                artigos = tabela_artigos.find_elements_by_class_name('searchArea')
                for artigo in artigos:
                    result = artigo.find_element_by_tag_name('td')
                    nome_artigo = result.find_element_by_tag_name('a').text
                    if nome_artigo == nome:
                        return artigo.find_elements_by_tag_name('td')[-1].text
                self._passa_pagina(pagina + 1)

        def _pesquisa_artigo(self, nome):
            """Insere o titulo e efetua a busca"""
            limpa = self.driver.find_element_by_id('txtBoxSearch')
            inp = limpa.find_element_by_id('searchterm1')
            inp.send_keys(nome)
            botao = self.driver.find_elements_by_class_name('btnText')
            botao[3].click()

        def principal(self, nomes_artigos):
            """Função Principal pro Site Scopus."""
            self._scopus()
            sleep(10)
            self.driver.find_element_by_id('_pendo-close-guide_').click()
            for pagina in range(len(nomes_artigos)):
                for numero, nome_artigo in enumerate(nomes_artigos[pagina]):
                    try:
                        limpa = self.driver.find_element_by_id('txtBoxSearch')
                        botao_limpa = limpa.find_element_by_tag_name('button')
                        botao_limpa.click()
                    except:
                        self._pesquisa_artigo(nome_artigo)
                        num_citacoes = self._procura_e_compara_artigo(nome_artigo)
                        self.citacoes.append((nome_artigo, num_citacoes))
                        self._scopus()
            return self.citacoes

    driver = webdriver.Chrome()  # Criação do webdriver do google.
    theend = Theend(driver)  # criação do objeto Theend.
    titulos_artigos = theend.principal()  # Retorna os títulos dos artigos
    scopus = Scopus(driver)  # Criação do objeto Scopus.
    scopus.principal(titulos_artigos)

if __name__ == "__main__":
    main()

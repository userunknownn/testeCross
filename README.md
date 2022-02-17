# Código do teste Cross Commerce

## Características :
    *Ao clicar na Api Numbers demorará entre 1 e 2 minutos*
    *Podendo variar dependendo da máquina*
    
    +Ao ser exibido o resultado este estará paginado pois o navegador
    dá erro se tiver carregando tantos resultados de uma vez.
    
    *para rodar a aplicação entre no terminal na pasta raiz*
    
    crie um ambiente virtual para o python:
        ´virtualenv venv´
    ative esse ambiente:
        ´source venv/bin/activate´
    instale as dependências:
        ´pip install -r requirements.txt´
    ainda no terminal entre na pasta Cross_Commerce:
        ´cd Cross_Commerce´
    rode o servidor: 
        ´python manage.py runserver´
    no terminal dirá onde estará a aplicação:
        ´ex : Starting development server at http://127.0.0.1:8000/´
    ao entrar existirá o link na tela:
        ´ "api/Numbers": "http://127.0.0.1:8000/api/Numbers/"´
    ao clicar nesse link, irá reunir as informações e após 
    o tempo de espera de 1 à 2 min, estas serão exibidas
    
    Uma vez que se tenha finalizado à utilização da aplicação,
    ainda no terminal , saia do ambiente virtual:
        ´deactivate´

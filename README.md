Zabbix Turbo Scripts
--------------------
Grupo de scripts e utilidades para uso em conjunto com o Zabbix, que permitem melhor integração e automação de tarefas.

Introdução
----------

Zabbix Turbo Scripts é um conjunto de scripts para facilitar o gerenciamento a automação de tarefas no Zabbix.

Atualmente, a seguinte solução é provida:

 * ITService: Criação automática de ITServices no Zabbix para todos as triggers que contenham o estado 'Desastre' e seus respectivos hosts e grupos de hosts;

Requerimentos
-------------

Para utilizar o Zabbix Turbo Scripts você vai precisar de um interpretador Python Instalado em seu SO, além do gerenciador de pacotes do python o PIP(http://https://pip.pypa.io/en/stable/installing/). 

Recomenda-se que você utilize um ambiente virtual (virtualenv),para a instalação das bibliotecas necessárias.


Instalação
----------

Primeiramente, clone este repositório para uma pasta com o seguinte commando:

``` git clone https://github.com/gcavalcante8808/zabbix-turbo-scripts ```

Acesse a pasta criada e execute o seguinte comando:

``` pip install -r requirements.txt ```


Utilização
----------

Uma vez que a instalação foi concluída com sucesso, você pode utilizar, por exemplo, o script de criação de ITServices da seguinte maneira:

``` python itservice.py -s http://<SERVIDOR>/ -u <USUARIO> (--passfile <ARQUIVO> ou -p) --http_auth <False> --purge <False> ```

Cada parâmetro passado, corresponde a seguinte informação:

 * Obrigatório -s: URL do frontend do Zabbix, no formato http://servidor/;
 * Obrigatório -u: Nome do Usuário do Zabbix. O usuário utilizado aqui somente poderá criar Serviços de TI para os grupos de hosts em que ele tenha acesso de escrita;
 * -p: Fará com que um prompt apareça pedindo a senha no terminal de maneira segura. Não pode ser usado em conjunto com --passfile.
 * --passfile: Ao invés de usar um prompt, procura a senha no arquivo especificado, útil para uso em scripts. Não pode ser usado em conjunto com -p;
 * --http_auth: Para os casos em que o Zabbix é configurado para utilizar autenticação HTTP (via webserver) ao invés de interna ou ldap. Devem ser utilizada a palavra True ou False.;
 * --purge_tree: permite excluir toda a árvore de Serviços de TI, mas requer que o usuário especificado seja administrador da ferramenta.

** O comportamento padrão do script é criar a árvore ou atualizar com novos itens criados **

** O script pode ser executado pelo próprio usuário do zabbix no Sistema Operacional ou outro usuário sem privilégios **

Assim, um exemplo de uso do script seria o seguinte:

** Criar ou atualizar uma árvore existente

``` python itservice.py -s http://localhost/ -u Admin --passfile /tmp/senha.txt ```

** Excluir uma árvore existente

``` python itservice.py -s http://localhost/ -u Admin --passfile /tmp/senha.txt --purge_tree True ```




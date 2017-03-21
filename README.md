Zabbix Itservice Scripts
------------------------

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

``` git clone https://github.com/gcavalcante8808/zabbix-turbo-scripts.git ```

Acesse a pasta criada e execute o seguinte comando:

``` pip install -r requirements.txt ```


Utilização
----------

Uma vez que a instalação foi concluída com sucesso, você pode utilizar, por exemplo, o script de criação de ITServices da seguinte maneira:

``` python itservice.py -s http://<SERVIDOR>/ -u <USUARIO> (--passfile <ARQUIVO> ou -p) --http_auth <False> --purge <False> ```

Cada parâmetro passado, corresponde a seguinte informação:

Information about each parameter are explained bellow:

Basic Parameters:

 * -s (mandatory): Zabbix Frontend URL in http format (https://myserver.com):
 * -u (mandatory): Zabbix User;
 * -p (mutually exclusive with --passfile) Zabbix User Password;
 * --passfile (mutually exclusive with -p) Text file that has the Zabbix User Password;

Extra Auth Parameters:

 * --http_auth: Para os casos em que o Zabbix é configurado para utilizar autenticação HTTP (via webserver) ao invés de interna ou ldap. Devem ser utilizada a palavra True ou False;

Filter Params:

 * --hostgroup: Filtragem de criação de ITServices para um hostgroup específico;
 * --sla: Valor de SLA a ser definido. 99.9 caso não o atributo não seja provido;
 * --priority: Valor mínimo das triggers, conforme https://www.zabbix.com/documentation/2.4/manual/api/reference/triggerprototype/object;
 * --filter: String that will be used to filter the triggers by its description;

Organisation Params (Allow to define tree possible levels in the tree before the content):

 * --root: Root name which all other objects will be created underneath;
 * --branch: Second level (After root) which all objects will be placed;
 * --node: Third (and last level, after branch) which all objects will be place;

Clear Options (Dangerous):

 * --purge_tree: Allows do destroy all SLA tree, which includes previous calculate SLA. Use with Caution..

** O comportamento padrão do script é criar a árvore ou atualizar com novos itens criados **

** O script pode ser executado pelo próprio usuário do zabbix no Sistema Operacional ou outro usuário sem privilégios **

Assim, um exemplo de uso do script seria o seguinte:

** Criar ou atualizar uma árvore existente

``` python itservice.py -s http://localhost/ -u Admin --passfile /tmp/senha.txt ```

** Excluir uma árvore existente

``` python itservice.py -s http://localhost/ -u Admin --passfile /tmp/senha.txt --purge_tree True ```




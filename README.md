# Coleta de Dados de contribuidores

Repositório para os script que coleta dados de contribuidores de projetos no
Github para fins acadêmicos.

Requisitos:
 - Python 3
 - [PyGithub](https://github.com/PyGithub/PyGithub)

Como executar:

```bash
python3 get_contributor_data.py -i repositorios.txt -o get_contributor_data.csv
```
Onde:

 - -i: arquivo com a lista de repositórios para a coleta. Vide arquivo
   *repositorios.txt* como um exemplo.
 - -o: nome do arquivo *CSV* com o resultado da coleta. Caso o mesmo nome seja
   informado o conteúdo será **sobrescrito**.


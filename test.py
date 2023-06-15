'''
файл для того что бы тестировать возможные решения и вспоминать как это все же работает
Ну ты сам знаешь 
'''
# эта команда нужна, для того что бы проверить где лежат библиотеки в venv, загрузились ли они
# python -c "import site; print(site.getsitepackages())" 


try:
    def mai(x):
        print (x + '134')

    # if 6 >5:
    #     print ('rt')
except:
    print('error')
finally:
    print('final')

mai(2)
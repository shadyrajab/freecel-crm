import asyncio
from datetime import datetime
from functions.crm import get_crm_panel
from database.update_crm import update_crm
import pytz

fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')

print(datetime.now(fuso_horario_brasil))

async def check():
    while True:
        now = datetime.now(fuso_horario_brasil)
        if now.hour == 23 and now.minute == 59:
            print('Função executada')
            dataHoraInicioCarga = f'{now.year}-{now.month}-{now.day} 00:00:00'
            dataHoraFimCarga = f'{now.year}-{now.month}-{now.day} 23:59:00'
            dataframe = get_crm_panel(dataHoraInicioCarga, dataHoraFimCarga)
            update_crm(dataframe)

            print('Função completa')

            await asyncio.sleep(60)
        
        else:
            pass

asyncio.run(check())

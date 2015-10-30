нужен питон < 3
Стандартный алгоритм использования:
1. Послать компоненты в ОМС
    пример: python send_request.py line_provision internet_access
2. Посмотреть полученный order_id (например 154), сгенерировать ответы
    python generate_responses.py 154 line_provision internet_access
3. Посылать ответы в нужном порядке, первый аргумент - первые буквы системы и метода. Второй - номер заказа. Третий -
номер компонента, если его опустить или написать all пошлется все что есть.
Посылать примерно так

python send_responses.py HV 154 all
python send_responses.py LC 154 all
python send_responses.py HA 154 all
python send_responses.py WF 154 all
python send_responses.py LO 154 all
python send_responses.py HC 154 all

Можно посылать отдельно по каждому компоненту, тогда вместо all указывать компоненты (instance_id)

Утилитки:
    get_attribute - выписать определнный атрибут для указанных компонентов (если не указаны, выписывает для всех)
    validate - проверяет валидность XML (с этим справляется и прошлая :) )


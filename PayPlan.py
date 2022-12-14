from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from calendar import isleap


beginDate = date(2022, 11, 28)                        #дата выдачи
endDate = date(2032, 3, 15)                          #дата окончания
duration = 120                                   #срок кредита в мес
baseBalanceIn = 4000000.00                         #сумма кредита
rate = 4                                      #льготная ставка
payDay = 15                                        #день платежа
monthsGracePeriod = 6                           #льготный период в мес
percentRateAfterGracePeriod = 7              #ставка после льготного периода
creditEscrowDate = ''                            # предполагаемая дата раскрытия счета Эскроу
creditEscrowRate = ''                           # ставка с учетом скидки по Эскроу
rate_ = float()                             # Использую как переменную для подстановки в формулу льготной ставки или полной
payed = 0                                  # Выплачено клиентом всего от части ОД
ostatok = baseBalanceIn                     # Остаток на начало периода
# date_startp - переменная, определяющая дату начала периода платежа (с какой даты считается платеж)
# date_endp - переменная, определяющая дату завершения периода платежа (по какую дату считается платеж)
# days_month - кол-во дней в периоде платежа
# days_year - дней в году


for i in range(duration):       # Кол-во платежей
    if i <= monthsGracePeriod:  # пока действует льготный период
        rate_ = rate
    else:  # полная ставка
        rate_ = percentRateAfterGracePeriod

    if beginDate.day < payDay:                                      # Если первый платеж в том же месяце, изменить
        fdate_endp = date(beginDate.year, beginDate.month, payDay)        # только день
    elif beginDate.month == 12:                                       # Если кредит выдан в декабре, то указать №месяца 1
        fdate_endp = date(beginDate.year+1, 1, payDay)                # и увеличить год на 1
    else:                                                           # Иначе увеличить месяц на 1
        fdate_endp = date(beginDate.year, beginDate.month+1, payDay)


    date_startp = fdate_endp + relativedelta(months=+i)
    date_endp = date_startp + relativedelta(months=+1)
    days_month = str(date_endp - date_startp)
    days_month = int(days_month.split()[0])

    if isleap(date_startp.year) is True:
        days_year = 366
    else:
        days_year = 355

    if i == 0:
        percents = round((((rate_ * days_month) / (100 * days_year)) * baseBalanceIn), 2)
        aQty = percents                             # 1-й платеж состоит только из %
    else:               # первично округленный аннуитетный платеж
        aQty = round((rate_ * baseBalanceIn / 1200) / (1 - (1 + (rate_ / 1200)) ** -(duration - 1)), 2)

        if aQty % 1 > 0:  # Итоговый округленный аннуитетный платеж
            aQty = int(aQty + 1)
        else:
            aQty = int(aQty)
        percents = round((((rate_ * days_month) / (100 * days_year) * ostatok)), 2)

    post = ostatok
    pQty = round((aQty - percents), 2)  # часть основного долга (ОД) платежа
    payed += round(pQty, 2)  # всего от части ОД выплачено
    ostatok = round((baseBalanceIn - round(payed, 2)), 2)                           # остаток на начало периода


    print(i, date_startp, date_endp, post,days_year, days_month, aQty, pQty, percents, sep=' | ')

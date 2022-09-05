def witholding(wage,period,status):
    fica_witholding=wage * 0.062
    meidcare_witholding=wage * 0.0145
    
    one_a = wage
    one_b = period
    one_c = wage * period

    
    one_d= w4_4a = 0.0 #TODO this needs to be fetched from db#
    one_e = one_c + one_d
    one_f = w4_4b = 0.0 #TODO this needs to be fetched from db#
    
    if status == 'MFJ':
        one_g = w4_setp2 = 12900
    else:
        one_g=8600
        
    one_h = one_f + one_g
    
    if (one_e - one_h)<=0:
        aawa = 0.0
    else:
        aawa = one_e - one_h
    
    one_i = aawa


    # base_witholding = 0
    # tax_bracket = 0
    # aawe = 0
    
#Single or Married Filing Separately Tax Table look up.
# def witholding(wage):
# def witholding(aawa, period):
    if status == "MFJ":
        if aawa >= 0 and aawa <12200:
            base_witholding = 0
            tax_bracket = 0
            aawe=0
        if aawa >= 12200 and aawa < 32100:
            base_witholding = 0
            tax_bracket =.1
            aawe=12200
        if aawa >= 32100 and aawa < 93250:
            base_witholding = 1990
            tax_bracket =.12
            aawe=32100
        if aawa >= 93250 and aawa < 184950:
            base_witholding = 9328
            tax_bracket =.22
            aawe=93250
        if aawa >= 184950 and aawa < 342050:
            base_witholding = 29502
            tax_bracket =.24
            aawe=184950
        if aawa >= 342050 and aawa < 431050:
            base_witholding = 67206
            tax_bracket =.32
            aawe=342050
        if aawa >= 431050 and aawa < 640500:
            base_witholding = 95686
            tax_bracket =.35
            aawe=431050
        if aawa >= 640500:
            base_witholding = 168993.5
            tax_bracket =.37
            aawe=640505
    
    if status == "MFS":
        if aawa >= 0 and aawa <3950:
            base_witholding = 0
            tax_bracket = 0
            aawe=0
        if aawa >= 3950 and aawa < 13900:
            base_witholding = 0
            tax_bracket =.1
            aawe=3950
        if aawa >= 13900 and aawa < 44475:
            base_witholding = 995
            tax_bracket =.12
            aawe=13900
        if aawa >= 44475 and aawa < 90325:
            base_witholding = 4664
            tax_bracket =.22
            aawe=44475
        if aawa >= 90325 and aawa < 168875:
            base_witholding = 14751
            tax_bracket =.24
            aawe=90325
        if aawa >= 168875 and aawa < 213375:
            base_witholding = 33603
            tax_bracket =.32
            aawe=168875
        if aawa >= 213375 and aawa < 527550:
            base_witholding = 47843
            tax_bracket =.35
            aawe=213375
        if aawa >= 527550:
            base_witholding = 157804.25
            tax_bracket =.37
            aawe=527550
    
    if status == "HH":
        if aawa >= 0 and aawa <10200:
            base_witholding = 0
            tax_bracket = 0
            aawe=0
        if aawa >= 10200 and aawa < 24400:
            base_witholding = 0
            tax_bracket =.1
            aawe=10200
        if aawa >= 24400 and aawa < 64400:
            base_witholding = 1420
            tax_bracket =.12
            aawe=24400
        if aawa >= 64400 and aawa < 96550:
            base_witholding = 6220
            tax_bracket =.22
            aawe=64400
        if aawa >= 96550 and aawa < 175100:
            base_witholding = 13293
            tax_bracket =.24
            aawe=96550
        if aawa >= 175100 and aawa < 219600:
            base_witholding = 32145
            tax_bracket =.32
            aawe=175100
        if aawa >= 219600 and aawa < 533800:
            base_witholding = 46385
            tax_bracket =.35
            aawe=219600
        if aawa >= 533800:
            base_witholding = 156355
            tax_bracket =.37
            aawe=533800
        
    fed_witholding = (base_witholding+(tax_bracket * (aawa - aawe))) / period
    
    cfica = str(0.062 * one_a)
    cmedicare =  str(0.0145 * one_a)
    
    #Make strings for printing
    gross_wage=str(one_a)
    netpay=str(round((one_a - fed_witholding-fica_witholding-meidcare_witholding),2))
    fica=str(fica_witholding)
    medicare=str(round(meidcare_witholding,2))
    tax_bracket=str(tax_bracket)
    fed_witholding = str(round(fed_witholding, 2))
    
    g2netpay = {"gwage":one_a, "netpay":float(netpay), "fedtax":float(fed_witholding), "fica":float(fica_witholding), "medicare":meidcare_witholding, "cfica": (0.062 * one_a), "cmedicare":(0.0145 * one_a) }
    
    return (g2netpay)
    # print (g2netpay)
    
    # print ("Gross wage: " + gross_wage + "\n" +"Net pay: " + netpay + "\n" + "Fed Tax: " + fed_witholding + "\n" + "FICA: " + fica + "\n" + "Medicare: " + medicare )
    # return "Gross Pay: ${gross_wage}<br> Net Pay: ${netpay}<br>Federal Income Tax Witholding: <strong>${fed_witholding}</strong><br> FICA: <strong>${fica}</strong><br> Medicare: <strong>${medicare}</strong><br>Corp FICA (upto wage of $142,800 wage in 2021): <strong>${cfica}</strong><br>Corp Medicare: <strong>${cmedicare}</strong>".format(gross_wage=gross_wage, netpay=netpay,fed_witholding=fed_witholding, fica=fica, medicare=medicare, cfica=cfica, cmedicare=cmedicare)
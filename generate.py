from helper import load_object

import os
import numpy as np
import pandas as pd

vocabs = load_object('vocabs_excel.pl')

def gen_word(tag):   
    while True:
        word = vocabs[tag].sample().to_string(index=False)
        if word!='NaN':
            return word
        
def gen_word_sum_sub(n):
    pbs=[]
    anws=[]
    for i in range(n):
        pb=""
        sbj1 = gen_word('ชื่อ')
        sbj2 = gen_word('ชื่อ')
        while True:
            if sbj1!=sbj2:
                break
            sbj2 = gen_word('ชื่อ')
        v1 = gen_word('กริยา')
        obj1 = gen_word('ผลไม้')
        obj2 = gen_word('ผลไม้')
        nn = gen_word('ลักษณะนาม')
        comp = gen_word('เปรียบ')
        adj = gen_word('วิเศษณ์')
        cen = gen_word('หน่วย')
        spc = gen_word('ตัวช่วย')
        if (np.random.choice([1,2])==1):
            o1,o2 = obj1,obj2
        else: 
            o1,o2 = sbj1,sbj2
        num1=np.random.randint(1,100)
        num2=np.random.randint(1,100)
        num3=np.random.randint(1,200)
        num4=np.random.randint(1,200)
        pb_sub1=[sbj1,v1,obj1,str(num1),nn," ",sbj2,v1,obj1,str(num2),nn," ",sbj1,v1,obj1,comp,"ทั้งหมดกี่",nn]
        pb_sub2=[sbj1,v1,obj1,str(num1),nn," ",sbj2,v1,obj1,comp,sbj1,str(num2),nn," ",sbj2,v1,obj1,"ทั้งหมดกี่",nn]
        pb_addsub1=[o1,adj,str(num3),cen," ",o2,adj,str(num4),cen," ",o1,adj,comp,o2,"เท่าไร"]
        pb_addsub2=[o1,adj,str(num3),cen," ",o2,adj,comp,o1,str(num4),cen," ",o2,adj,"เท่าไร"]
        pb_add1=[sbj1,v1,obj1,str(num1),nn," ",sbj2,v1,obj1,str(num2),nn," ",sbj1,"และ",sbj2,v1,obj1,"รวมกันกี่",nn]
        pb_add2=[sbj1,v1,obj1,str(num1),nn," ",v1,obj1,spc,str(num2),nn," ","รวม",sbj1,v1,obj1,"ทั้งหมดกี่",nn]
        pb = np.random.choice([pb_sub1,pb_sub2,pb_addsub1,pb_addsub2,pb_add1,pb_add2])
        anw=0
        if (pb in [pb_add1,pb_add2]) or (pb==pb_sub1 and comp=='รวมกับ') or (pb==pb_sub2 and comp=='มากกว่า'):
            anw=num1+num2
        elif (pb==pb_addsub1 and comp=='รวมกับ') or (pb==pb_addsub2 and comp=='มากกว่า'):
            anw=num3+num4
        elif (pb==pb_addsub1 and comp=='มากกว่า') or (pb==pb_addsub2 and comp=='น้อยกว่า'):
            anw=num3-num4
        elif (pb==pb_addsub1 and comp=='น้อยกว่า') or (pb==pb_addsub2 and comp=='รวมกับ'):
            anw=num4-num3
        elif (pb==pb_sub1 and comp=='มากกว่า') or (pb==pb_sub2 and comp=='น้อยกว่า'):
            anw=num1-num2
        elif (pb==pb_sub1 and comp=='น้อยกว่า') or (pb==pb_sub2 and comp=='รวมกับ'):
            anw=num2-num1
        pbs.append(pb)
        anws.append(anw)
    return pbs, anws

def gen_word_mul(n):
    pbs=[]
    anws=[]
    for i in range(n):
        sbj1 = gen_word('ชื่อ')
        sbj2 = gen_word('ชื่อ')
        while True:
            if sbj1!=sbj2:
                break
            sbj2 = gen_word('ชื่อ')
        v1 = gen_word('กริยา')
        obj1 = gen_word('ผลไม้')
        obj2 = gen_word('ผลไม้')
        nn = gen_word('ลักษณะนาม')
        comp = gen_word('เปรียบ')
        adj = gen_word('วิเศษณ์')
        cen = gen_word('หน่วย')
        spc = gen_word('ตัวช่วย')
        pack = gen_word('กลุ่ม')
        num1 = np.random.randint(1,100)
        num2 = np.random.randint(1,100)
        pb=[sbj1,v1,obj1,str(num1),pack," ",pack,"ละ",str(num2),nn," ",sbj1,v1,obj1,"กี่",nn]
        anw=num1*num2
        pbs.append(pb)
        anws.append(anw)
    return pbs,anws

def gen_word_div(n):
    pbs=[]
    anws=[]
    for i in range(n):
        sbj1 = gen_word('ชื่อ')
        v1 = gen_word('กริยา')
        obj1 = gen_word('ผลไม้')
        nn = gen_word('ลักษณะนาม')
        pack = gen_word('กลุ่ม')
        num2 = np.random.randint(1,100)
        anw = np.random.randint(1,25)
        num1 = num2*anw
        pb_div1 = [sbj1,v1,obj1,str(num1),nn," ","จัดลง",pack," ",pack,"ละ",str(num2),nn," ",sbj1,v1,obj1,"กี่",pack]
        pb_div2 = [sbj1,v1,obj1,str(num1),nn," ","แบ่งลง",str(num2),pack," ",pack,"ละเท่าๆ กัน"," ",sbj1,"มี",obj1,pack,"ละ","กี่",nn ]
        pb = np.random.choice([pb_div1,pb_div2])
        pbs.append(pb)
        anws.append(anw)
    return pbs,anws

def gen_word_complex(n):
    pbs=[]
    anws=[]
    for i in range(n):
        sbj1 = gen_word('ชื่อ')
        v1 = gen_word('กริยา')
        obj1 = gen_word('ผลไม้')
        obj2 = gen_word('ผลไม้')
        nn = gen_word('ลักษณะนาม')
        nn2 = gen_word('ลักษณะนาม')
        num1=np.random.randint(1,100)
        buff=np.random.randint(1,25)
        num2=num1*buff
        num3=np.random.randint(1,100)
        pb_div2 = [sbj1,v1,obj1,str(num1),nn," ","ซื้อ",obj2,"ได้",str(num2),nn2," ",obj1,str(num3),nn,"ซื้อ",obj2,"ได้กี่",nn2]
        pbs.append(pb_div2)
        anw=(num2/num1)*num3
        anws.append(anw)
    return pbs, anws

def gen_word_problems(n):
    pbs=[]
    sens=[]
    anws=[]
    m = n//5
    pb,anw = gen_word_sum_sub(m*2)
    pbs+=pb
    anws+=anw
    pb,anw = gen_word_mul(m)
    pbs+=pb
    anws+=anw
    pb,anw = gen_word_div(m)
    pbs+=pb
    anws+=anw
    pb,anw = gen_word_complex(m)
    pbs+=pb
    anws+=anw
    for sentence in pbs:
        sens.append("".join(sentence))
    return (pbs,sens,anws)

def gen_auto(n):
    #run this one to gen pbs
    #n is number of problems
    m = n//5
    token,sentence,answer = gen_word_problems(n)
    t = ['s']*(m*2)+['m']*m+['d']*m+['c']*m
    data = pd.DataFrame({'problems':sentence,'tokenizes':token,'types':t, 'answers': answer})
    return data
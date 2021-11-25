
import os
import random


class rule :          #class règle
    conclusion=[]
    def __init__(self,premisses,conclusion):
        self.premisses=premisses
        self.conclusion=conclusion
        self.ruleID=0
    
    def afficher(self) : 
        i=0
        pstr=''
        while i < len(self.premisses) : 
            pstr+=self.premisses[i]+' ,'
            i+=1           
        print('si',pstr,' alors',self.conclusion)

class Fait:                #class Fait
    def __init__(self,fait):
        self.fait=fait
        self.flag=-1
    
    def afficher(self) : 
        print(self.fait,' ,explication: ',self.flag)

def clean_et(l):                     #clean list from 'et'
    f=l.split()
    while 'et' in f : 
        f.remove('et')
    return f

def extract_BR(path):                      #extraire la base des faits à partir d'un fichier texte
    BR=[]
    f=open(path,'r',encoding='utf-8')
    lines = f.readlines()
    f.close()
    lines=[line.strip('\n') for line in lines]
    i=0
    while i<len(lines):
        lp=clean_et(lines[i].split('alors')[0])
        lp.remove('si')
        lc=clean_et(lines[i].split('alors')[1])
        rule(lp,lc)
        r=rule(lp,lc)
        r.ruleID=i+1
        BR.append(r)
        i+=1
    return BR

def extract_BF(path):                      #extraire la base des faits à partir d'un fichier texte
    BF=[]
    f=open(path,'r',encoding='utf-8')
    lines = f.readlines()
    f.close()
    lines=[line.strip('\n') for line in lines]
    i=0
    while i<len(lines):
        l=lines[i].split().pop(1).split(',')
        j=0
        while j<len(l):
            f=Fait(l[j])
            BF.append(f)
            j+=1
        i+=1
    return BF
    

def abs_path(rel_path):                 #return absolute path
    script_dir = os.path.dirname(__file__)
    path = os.path.join(script_dir, rel_path)
    return path


def app_rules(BR,temp):           #extract appliable rules
    app_list=[]
    i=0
    for i in range(len(BR)):
        r_premisse=BR[i].premisses
        j=0
        for j in range(len(r_premisse)):
            TF=r_premisse[j] in temp
            if TF==False:
                break
        app_list.append(TF)
    return app_list


def unique_list(BR,temp):    #extract a list of unique premisses and conclusion and intial premisses
    i=0
    l=temp.copy()
    while i < len(BR):
        rule=BR[i]
        for p in range(len(rule.premisses)):
            if ((rule.premisses[p] in temp)==False)&((rule.premisses[p] in l)==False) : 
                l.append(rule.premisses[p])
        for c in range(len(rule.conclusion)):
            if ((rule.conclusion[c] in temp)==False)&((rule.conclusion[c] in l)==False) :
                l.append(rule.conclusion[c])
        i+=1
    return l 


def chainage_avant(BR,BF,temp,goal,user_ConfRes,log_check):  #apply the algorithm
    i=0
    j=0
    ul=unique_list(BR,temp)
    log= open("log.txt", "w",encoding='utf-8')   
    l=[]
    if goal:
        if goal in temp:
            print('***** Le but existe déja dans la base des faits *****')
            l.append('***** Le but existe déja dans la base des faits *****')
            log.writelines(l)
            stop=True
    if (any(app_rules(BR,temp)))==False : 
        print('***** On ne peut pas avancer, aucune règle n''est appliquable *****')
        l.append('***** On ne peut pas avancer, aucune règle n''est appliquable *****')
        log.writelines(l)
    while (any(app_rules(BR,temp))) :
        i+=1
        ######choosing the rule depending on the user choice##########
        if user_ConfRes=='Random':
            randlist=[]
            for k in range(len(app_rules(BR,temp))):
                if app_rules(BR,temp)[k]:
                    randlist.append(k)
            chosen_rule=randlist[random.randrange(len(randlist))]       
        if user_ConfRes=='Reverse':
            chosen_rule=len(app_rules(BR,temp))-app_rules(BR,temp)[::-1].index(True)-1
        else:
            chosen_rule=app_rules(BR,temp).index(True)
            ##########################################################
        ######## add conclusions to base and check if conclusion already exists#########
        for j in range(len(BR[chosen_rule].conclusion)):
            new_fait=Fait(BR[chosen_rule].conclusion[j])
            new_fait.flag=BR[chosen_rule].ruleID
            if new_fait.fait in temp:
                continue
            BF.append(new_fait)
            temp.append(new_fait.fait)
            ###########################################################
            ######### writing in log ############
        l=[]
        l.append('règle appliqué : '+str(BR[chosen_rule].ruleID)+'\n')
        l.append('itération num '+str(i)+' ,nouvelle BF : '+'\n')
        l.append('['+' , '.join(temp)+']'+'\n')
        l.append('----------------------- \n')
        print('règle appliqué : ',BR[chosen_rule].ruleID)
        print('itération num ',i,',nouvelle BF : ')
        print(temp)
        if len(temp)==len(ul):
            print('***** Base saturé *****')
            l.append('***** Base saturé *****')
        print('------------------------')
        ########################################
        ######### check for goal ###########
        if goal:
            if goal in temp:
                print('***** but atteint *****')
                l.append('***** but atteint *****')
                log.writelines(l)
                break #break if goal reched
        del BR[chosen_rule] #deleting the used rule
        if (any(app_rules(BR,temp)))==False : 
            print('***** On ne peut pas avancer. La base est saturé*****')
            l.append('***** On ne peut pas avancer. La base est saturé*****')
        if log_check==True :
            log.writelines(l)
    log.close()
    
    
#recurssive algotithm for prooving goal using 'chainage arriere'
def proove(BR,temp,prem,conflict_Res,lines):
    
    lines.append('-----------------------------'+'\n')
    print('-----------------------------')
    #b is boolean to test the validity of path taken by the algorithm
    b=False
    l=search_goal(BR,prem)
    lines.append('rules with '+prem+' as goal. '+listToString(l)+'\n')
    print('rules with '+prem+' as goal. ', l)
    
    if len(l)==0:
        lines.append('no rule with said goal'+'\n')
        print('no rule with said goal')
        return False
    
    #if a path is a dead end repeat with another rule until b is true
    while (b==False) & (len(l)!=0):
        lines.append('-----------------------------'+'\n')
        print('-----------------------------')
        chosen_rule=conflict(l,conflict_Res)
        lines.append('chosen rule : '+str(chosen_rule)+'\n')
        print('chosen rule : ',chosen_rule)
        prem_to_proove=goal_realisable(BR,temp,chosen_rule)
        lines.append('premisses to proove '+listToString(prem_to_proove)+'\n')
        print('premisses to proove',prem_to_proove)
        
        if len(prem_to_proove)==0:
            lines.append('goal prooven with database'+'\n')
            print('goal prooven with database')
            return True
        
        #proove with rules.
        else:
            i=0
            b=True
            #
            while i<len(prem_to_proove):
                b=b and proove(BR,temp,prem_to_proove[i],conflict_Res,lines)
                i=i+1
            if b==False : 
                lines.append('Dead end'+'\n')
                print('Dead end')
                        
    return b 

### ensmble S / returns ruleIds of rules with said goal
def search_goal(BR,goal):
    l=[]
    for i in range(len(BR)):
        if (goal in BR[i].conclusion):
            l.append(BR[i].ruleID)
    return(l)

#returns list with premisses to proove
def goal_realisable(BR,temp,rid): 
    l=[]
    for i in range(len(BR)):
        if BR[i].ruleID==rid :
            rule=BR[i]
    for i in range(len(rule.premisses)):
        if rule.premisses[i] in temp:
            continue
        l.append(rule.premisses[i])
    else:
        return(l)
    
#### Define conflicts
def conflict(l,choice):
    if choice=='':
        return(l.pop(0))
    if choice=='Reverse':
        return(l.pop(len(l)-1))
    else:
        return 0

def listToString(s): 
    str1 = "[ " 
    # traverse in the string  
    for ele in s: 
        str1 += (str(ele)+' ') 
    str1 += ']'
    return str1 

def chainage_arriere(BR,temp,goal,confRes,log_check):
    p=search_goal(BR,goal)
    if len(p)==0 :
        print('le but n''existe pas')
    else:
        #log file
        log= open("log_arriere.txt", "w",encoding='utf-8')   
        lines=[]
        #algorithm ipmlementation
        proove(BR,temp,goal,confRes,lines)
        if log_check:
            log.writelines(lines)
            log.close()
        
        






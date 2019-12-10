import sys

def leetify(i, a):
    
    if len(a)>0:
        c=a[0]
        
        d=c.lower()

        leetify(i+c,a[1:])

        if d=='o':
            leetify(i+'0',a[1:])

        if c=='e':
            leetify(i+'3',a[1:])
        
        if d=='s':
            leetify(i+'5',a[1:])
            leetify(i+'$',a[1:])

        if c=='a':
            leetify(i+'@',a[1:]) 
            
        if c=='A':
            leetify(i+'4',a[1:])
            
        if d=='i' or c=='l':
            leetify(i+'1',a[1:])
                                   
    else:
        print(i)
        

with open(sys.argv[1],'r', encoding="utf-8") as inpfile:
    l = inpfile.readline()
       
    while l:
        try:
            leetify('',l.rstrip())
            l = inpfile.readline()
        except:
            print(l.rstrip)
            

def ValueCard(s,Trump) :
 v = 0
 if s[0] == '6': 
  v = 6
 elif s[0] == '7':
  v = 7
 elif s[0] == '8':
  v = 8    
 elif s[0] == '9':
  v = 9
 elif s[0] == '1':
  v = 10                
 elif s[0] == 'J':
  v = 11                        
 elif s[0] == 'Q':
  v = 12
 elif s[0] == 'K':
  v = 13    
 elif s[0] == 'A':
  v = 14
 if s[-1] == Trump[-1]:
  v+=1
  
 return v


def Utility(hand,Trump) :
 S = 0 
 for i in range(len(hand)):
  S += ValueCard(hand[i],Trump)
  
 return S
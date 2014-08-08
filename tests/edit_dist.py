#coding:utf-8
#Levenshtein 编辑距离算法
import sys
#快速算法，节约内存，只能提供编辑距离
def LevenshteinDistance(s, t):
    if (s == t):
        return 0
    if (len(s) == 0):
        return t.Length;
    if (len(t) == 0):
        return s.Length;

    v0 = [0]*(len(t) + 1);
    v1 = [0]*(len(t) + 1);
    for i in xrange(len(v0)):
        v0[i] = i

    for i in xrange(len(s)):
        v1[0] = i + 1;
        for j in xrange(len(t)):
            cost = 0 if s[i] == t[j] else 1
            #                     del         add              modify
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)

        v2=v0
        v0=v1
        v1=v2

    return v0[len(t)];
#完整算法，提供编辑距离，转换矩阵，编辑路径，需要编辑路径的时候使用
def LevenshteinDistance2(s,t):
    m=len(s)
    n=len(t)
    d=[[0]*(n+1) for i in xrange(m+1)]

    for i in xrange(1,m+1):
        d[i][0] = i

    for j in xrange(1,n+1):
        d[0][ j] = j

    for j in xrange(1,n+1):
      for i in xrange(1,m+1):
          if s[i-1] == t[j-1]:
              d[i][j] = d[i-1][ j-1]
          else:
              d[i][j] = min(
                      d[i-1][j],# a deletion
                      d[i][j-1],  # an insertion
                      d[i-1][j-1]  # a substitution
                )+1

    max_step=d[m][n]
    rount=[]
    checked=set()
    def findnextrount(i,j,rount):
        if (i,j) in checked:
            return False
        checked.add((i,j))
        if i==0 and j==0:
            return True
        now=d[i][j]
        if now>max_step:
            return False
        if i==0:
            delete=sys.maxint
        else:
            delete=d[i-1][j]

        if i==0 or j==0:
            replace=sys.maxint
        else:
            replace=d[i-1][j-1]

        if j==0:
            insert=sys.maxint
        else:
            insert=d[i][j-1]

        if replace<=max_step and (replace<now or (replace==now and s[i-1]==t[j-1])):
                if findnextrount(i-1,j-1,rount):
                    if now==replace:
                        rount.append((i,j,'kep',s[i-1]))
                    else:
                        rount.append((i,j,'rep',s[i-1],t[j-1]))
                    return True
        if delete<=max_step and delete<now:
            if findnextrount(i-1,j,rount):
                rount.append((i,j,'del',s[i-1]))
                return True
        if insert<=max_step and insert<now:
            if findnextrount(i,j-1,rount):
                rount.append((i,j,'add',t[j-1]))
                return True
        return False
    findnextrount(m,n,rount)
    return max_step,d,rount


a=u'Sunday'
b=u'Sturday'
data= LevenshteinDistance2(a,b)
for one in data[1]:
    print one
for one in data[2]:
    print(one)
print data
print LevenshteinDistance(a,b)

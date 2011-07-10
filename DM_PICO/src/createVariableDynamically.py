#for i in range(2,4):
listMy = ['a', 'b', 'c']
listMyVar =[]
for i in range(0,len(listMy)):
#    print 'i: ', i
    exec 'var%s = %s*10' % (listMy[i], i)
    exec "listMyVar.append(var%s)" % (listMy[i])
#    exec "print 'var%s' var%s" % (listMy[i], listMy[i])
#    exec "print var%s" % (listMy[i])
#    exec "print 'var%s =', var%s" % (listMy[i], listMy[i])
#    print 'varb = ', vara
print 'listMyVar: ', listMyVar
import morfeusz2

morf = morfeusz2.Morfeusz()
input = u"Rozmawiałem na giełdzie."

for word in input.split():
    analyzed = morf.analyse(word)
    for a in analyzed:
        if not a[2][2].startswith('subst'):
            continue
        print(word)
        print(analyzed)
        print(a[2])
        print()
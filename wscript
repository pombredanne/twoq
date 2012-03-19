top = '.'
out = 'build'

# http://docs.waf.googlecode.com/git/book_16/single.html#_introduction

def configure(ctx):
        print('→ configuring the project in ' + ctx.path.abspath())

def build(ctx):
    ctx(rule='hg update pu')
    ctx(rule='hg update next')
    ctx(rule='hg merge pu; hg ci -m automerge')
    ctx(rule='hg update maint')
    ctx(rule='hg merge default; hg ci -m automerge')
    ctx(rule='hg update default')
    ctx(rule='hg merge next; hg ci -m automerge')
    ctx(rule='hg update pu')
    ctx(rule='hg merge default; hg ci -m automerge')
#    prompt('Enter tag:', 'tag')
#    with settings(warn_only=True):
    ctx(rule='hg tag "%(tag)s"')  # % env)
    ctx(rule='hg push ssh://hg@bitbucket.org/lcrees/twoq')
    ctx(rule='hg push git+ssh://git@github.com:kwarterthieves/twoq.git')
    ctx(rule='python setup.py register sdist --format=bztar,gztar,zip upload')
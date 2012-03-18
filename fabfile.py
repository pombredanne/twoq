'''twoq fabfile'''

from fabric.api import prompt, local, settings, env


def tox():
    '''test twoq'''
    local('tox')


def release():
    '''release twoq'''
    local('hg update pu')
    local('hg update next')
    local('hg merge pu; hg ci -m automerge')
    local('hg update maint')
    local('hg merge default; hg ci -m automerge')
    local('hg update default')
    local('hg merge next; hg ci -m automerge')
    local('hg update pu')
    local('hg merge default; hg ci -m automerge')
    prompt('Enter tag', 'tag')
    with settings(warn_only=True):
        local('hg tag "%(tag)s"' % env)
        local('hg push ssh://hg@bitbucket.org/lcrees/twoq')
        local('hg push git+ssh://git@github.com:kwarterthieves/twoq.git')
#    local('python setup.py register sdist --format=bztar,gztar,zip upload')

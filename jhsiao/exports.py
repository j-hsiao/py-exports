"""Varous helper functions for managing __all__

__all__ should be at module scope. In module scope, locals() and
globals() return the same thing and globals() is always guaranteed
to "Return the dictionary implementing the current module namespace."
(same dict).
"""
from __future__ import print_function
__all__ = ['public']
from .scope import Scope

def public(all_=None):
    """Return a decorator that adds item.__name__ to all_.

    if all_ is None, also create and return a list to act as
    __all__
    example:
        __all__ = []
        @public(__all__)
        class myclas(object):
            pass
        public = exports.public(__all__)
        @public
        def myfunc():
            pass
        public, __all__ = exports.public()
    """
    def public(item):
        all_.append(item.__name__)
        return item
    if all_ is None:
        all_ = []
        return public, all_
    return public

@public(__all__)
def public_end(globs, initial='public_begin'):
    """Add diff of globs and globs[initial] to globs['__all__'].

    NOTE: <initial> should create a copy of the current locals() keys
        or globals() may be updated and then there is no way to tell
        which names were added.

    <initial> is the name of the original set(locals()).  Assumes that
    __all__ is in globs.  This does not require objects to have a
    __name__ attribute and requires only 2 additional lines (excluding
    the import)

    example usage:
        __all__ = []
        public_begin = set(locals())
        MY_CONST = 9001
        class myclass(object):
            pass
        def myfunc():
            pass
        public_end(locals())
        __all__ == ['MY_CONST', 'myclass', 'myfunc']
    """
    diffs = set(globs).difference(globs[initial])
    diffs.discard(initial)
    globs['__all__'].extend(diffs)

class PublicScope(Scope):
    """A Scope that adds new names to __all__ at context end."""
    def __exit__(self, exctp, exc, tb):
        lst = self.pframe.f_locals.get('__all__')
        if lst is not None:
            lst.extend(self.diff())
        super(PublicScope, self).__exit__(exctp, exc, tb)


if __name__ == '__main__':
    import sys
    from jhsiao import exports
    # Use public as decorator.
    public = exports.public
    __all__ = []
    @public(__all__)
    class pubclass(object):
        pass
    @public(__all__)
    def pubfunc():
        pass
    assert __all__ == ['pubclass', 'pubfunc']

    # Use exporter.
    public, __all__ = exports.public()
    @public
    class expclass(object):
        pass
    @public
    def expfunc():
        pass
    assert __all__ == ['expclass', 'expfunc']

    # Use begin/end method.
    __all__ = []
    public_begin = set(locals())
    class begclass(object):
        pass
    def begfunc():
        pass
    begvar = 9001
    public_end(locals())
    assert set(['begclass', 'begfunc', 'begvar']) == set(__all__)

    __all__ = []
    with PublicScope():
        jfeqwghad = 1
        qhagdkjzvxcg = 2
    assert sorted(__all__) == ['jfeqwghad', 'qhagdkjzvxcg']

    print('pass', file=sys.stderr)

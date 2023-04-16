from lark import Token, Tree

Tree(
    Token('RULE', 'p'),
    [
        Tree('define', [Tree(Token('RULE', 'var'), [Token('__ANON_0', 'x')])]),
        Tree(
            Token('RULE', 'p'),
            [
                Tree(
                    'assign',
                    [
                        Tree(Token('RULE', 'var'), [Token('__ANON_0', 'base')]),
                        Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'int'), [Token('SIGNED_INT', '2')])])
                    ]
                ),
                Tree(
                    Token('RULE', 'p'),
                    [
                        Tree(
                            'assign',
                            [
                                Tree(Token('RULE', 'var'), [Token('__ANON_0', 'log')]),
                                Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'int'), [Token('SIGNED_INT', '0')])])
                            ]
                        ),
                        Tree(
                            Token('RULE', 'p'),
                            [
                                Tree(
                                    'if',
                                    [
                                        Tree(
                                            'gt',
                                            [
                                                Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'var'), [Token('__ANON_0', 'x')])]),
                                                Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'int'), [Token('SIGNED_INT', '0')])])
                                            ]
                                        ),
                                        Tree(
                                            Token('RULE', 'p'),
                                            [
                                                Tree(
                                                    'while',
                                                    [
                                                        Tree(
                                                            'gt',
                                                            [
                                                                Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'var'), [Token('__ANON_0', 'x')])]),
                                                                Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'int'), [Token('SIGNED_INT', '1')])])
                                                            ]
                                                        ),
                                                        Tree(
                                                            Token('RULE', 'p'),
                                                            [
                                                                Tree(
                                                                    'assign',
                                                                    [
                                                                        Tree(Token('RULE', 'var'), [Token('__ANON_0', 'log')]),
                                                                        Tree(
                                                                            'add',
                                                                            [
                                                                                Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'var'), [Token('__ANON_0', 'log')])]),
                                                                                Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'int'), [Token('SIGNED_INT', '1')])])
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),
                                                                Tree(
                                                                    'assign',
                                                                    [
                                                                        Tree(Token('RULE', 'var'), [Token('__ANON_0', 'x')]),
                                                                        Tree(
                                                                            'div',
                                                                            [
                                                                                Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'var'), [Token('__ANON_0', 'x')])]),
                                                                                Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'var'), [Token('__ANON_0', 'base')])])
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                Tree(
                                    Token('RULE', 'p'),
                                    [
                                        Tree(
                                            'assign',
                                            [
                                                Tree(Token('RULE', 'var'), [Token('__ANON_0', 'log')]),
                                                Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'int'), [Token('SIGNED_INT', '-1')])])
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        Tree(Token('RULE', 'p'), [Tree('print', [Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'var'), [Token('__

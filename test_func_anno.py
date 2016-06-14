#/usr/bin/env python3
import unittest


def type_check(func):
    '''Decorator for enforcing type checking based on Python 3.0 annotations
    '''
    def annotation_wrapper(*arg, **kw):
        for i, arg_val in enumerate(arg):
            arg_name = func.__code__.co_varnames[i]
            if not isinstance(arg_val, func.__annotations__[arg_name]):
                raise TypeError('Expecting %r type for %r argument' % 
                                (func.__annotations__[arg_name], arg_name)) 
                               
        for arg_name, arg_val in kw.items():
            if not isinstance(arg_val, func.__annotations__[arg_name]):
                raise TypeError('Expecting %r type for %r keyword argument' % 
                                (func.__annotations__[arg_name], arg_name))
            
        ret = func(*arg, **kw)
        if not isinstance(ret, func.__annotations__['return']):
            raise TypeError('Expecting %r type for return' %
                            func.__annotations__['return'])
            
        return ret
        
    return annotation_wrapper


@type_check
def my_func(x: str, num: int, y: float = 1.0, b: bool = False) -> str:
    """Test type checking decorator based on function annotations"""
    return x + str(num * y or b)


class TestFunctionAnnotationsDecoratorTestCase(unittest.TestCase):
    def test_succeed_default_kw(self):
        self.assertTrue(my_func('x', 0))

    def test_succeed_all_kw(self):
        self.assertTrue(my_func('y', 34, y=7., b=True))

    def test_succeed_1st_kw(self):
        self.assertTrue(my_func('z', 9, y=720.))

    def test_succeed_2nd_kw(self):
        self.assertTrue(my_func('x', 6, b=True))
    
    def test_fail_arg1(self):
        self.assertRaises(TypeError, my_func, 0, 6, b=True)
    
    def test_fail_arg2(self):
        self.assertRaises(TypeError, my_func, 'x', 'y', b=True)
    
    def test_fail_arg3(self):
        self.assertRaises(TypeError, my_func, 'x', 20, y=8, b=True)
        
    def test_fail_arg4(self):
        self.assertRaises(TypeError, my_func, 'x', 20, y=8, b=True)
  

if __name__ == "__main__":
    unittest.main()

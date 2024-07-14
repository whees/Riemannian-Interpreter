# Command Line Riemannian Geometry Interpreter

This code provides an environment to perform calculations relevant to Riemannian Geometry.

## Supported Operations 
|Symbol  |Function                      |
|:-----  |:-------------------------    |
| +      | addition                     |
| -      | subtraction                  |
| *      | multiplication               |
| /      | division                     |
| ^      | exponentiation               |
| &      | functional differentiation   |
| $      | partial differentiation      |
| log    | natural logarithm            |
| =      | assignment                   |
| show   | output to console            |
| diag   | create a diagonal tensor     |

<!-- USAGE EXAMPLES -->
## Usage
* Variables are assigned via the '=' operator. The function immediately to the right of an '=' operator will be assigned to the variable immedately to the left of the operator. A variable's assignment is simplified upon construction.
```
> y=x*x
```
* The assignment of the variable (in parentheses) immediately to the right of a 'show' operator will be shown. The assignment will be printed to the following line.
```
> y=x*x
> show(y)
(x)^(2)
```
*  Unassigned variables will be treated as general functions. Assigned variables will be automatically substituted in later operations.
```
> y=x*x
> z=y*y
> show(z)
(x)^(4)
```
* Multiple statements on the same line are separeted by a semi-colon. Multi-statement lines will be executed from left to right.
```
> y=x*x; z=y*y
> show(z)
(x)^(4)
```
* A functional derivitive is performed on the expression immediately to the right of an '&' operator. In the output, '&[]' represents the variation of function '[]'.
```
> y=&(x*x)
> show(y)
> (x)*(&x)*(2)
```
* A partial derivitive is performed on the expression (in parentheses) immediately to the right of a '$_[]' operator with respect to variable/function '[]'.
```
> y=$_x(x*x)
> show(y)
(x)*(2)
```
* A logarithm of natural base is perormed on the expression (in parentheses) immediately to the right of the 'log' operator.
```
> y=$_x(log(x))
> show(y)
(x)^(-1)
```
* A diagonal tensor is constructed via a 'diag([])^{}' command, and can be assigned to a variable via '='. 'diag([])^{}' constructs a diagonal tensor with {} indices that range through [] variables. By default, this tensor is the metric tensor for {} dimensional Euclidean space (all ones). Non-diagonal elements DO NOT EXIST in a diagonal tensor, since they are always zero by construction.
```
> T=diag(x,y)^2
> show(T[x,x])
1
```


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Big shoutout to Ruslan Spivak for the tutorial on building interpreters. Their blog post at https://ruslanspivak.com/lsbasi-part1/ is super informative.

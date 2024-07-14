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
| []     | reference                    |
| show   | output to console            |
| dime   | create a diagonal metric     |

<!-- USAGE EXAMPLES -->
## Usage
* Variables are assigned via the '=' operator. The function immediately to the right of an '=' operator will be assigned to the variable immedately to the left of the operator.
* A line is executed upon the press of 'enter'.
```
> y=x*x
>
```
* A variable's assignment is simplified upon construction.
* The assignment of a variable (in parentheses) immediately to the right of a 'show' operator will be shown. The assignment will be printed to the following line.
```
> y=x*x
> show(y)
(x)^(2)
```
*  Unassigned variables will be treated as general functions. Assigned variables will be substituted into later operations.
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
* A functional derivitive is performed on the expression immediately to the right of an '&' operator. In the output, '&□' represents the variation of function '□'.
```
> y=&(x*x)
> show(y)
> (x)*(&x)*(2)
```
* A partial derivitive is performed on the expression (in parentheses) immediately to the right of a '$_□' operator, with respect to variable/function '□'.
```
> y=$_x(x*x)
> show(y)
(x)*(2)
```
* A logarithm of natural base is performed on the expression (in parentheses) immediately to the right of the 'log' operator.
```
> y=$_x(log(x))
> show(y)
(x)^(-1)
```
* A diagonal metric tensor is constructed via a 'dime' command, and can be assigned a name via '='.
* 'dime(□)' constructs a diagonal metric labeled by the list of variables '□'.
```
> g=dime(x,y)
>
```
* By default, a diagonal tensor is the metric tensor for N-dimensional Euclidean space, where N denotes the length of the passed list of variables. 
* Tensor elements can be referenced via the reference operator '[□]', which retrieves element '□'.
* Tensor elements can be assigned a value via the '=' operator.
* NOTE: Elements are referenced by a single instance of their label to avoid redundancy. For example, g[x] denotes the 'xx' component of g.
```
> g=dime(x,y)
> show(g[x])
1
> g[x]=1+u
> show(g[x])
1+(u)
```


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Big shoutout to Ruslan Spivak for the tutorial on building interpreters. Their blog post at https://ruslanspivak.com/lsbasi-part1/ is super informative.

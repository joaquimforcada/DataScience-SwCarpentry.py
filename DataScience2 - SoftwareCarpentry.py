
# coding: utf-8

# Software Carpentry
# ==================
# 
# ##What does Software Carpentry stands for?
# 
# In order to be an efficient Data Scientist you need a chain of tools and a methodology for using it:

# 
# 
# * Programming Language - Python (&#10004;)
# * Command-Line Programs and IDE's (&#10008;)
# * Defensive Programming (&#10008;)
# * Debugging (&#10008;)
# * Profiling (&#10008;)
# * Version Control (&#10008;)
# 
# Further Sessions:
# * NoSQL Database 
# * Web Scrapping 
# * Numpy + Pandas 
# 
# 
# 

# #Executing Python Scripts
# 
# The IPython Notebook and other interactive tools are great for prototyping code and exploring data,
# but sooner or later we will want to use our program in a pipeline
# or run it in a shell script to process thousands of data files.
# In order to do that, we need to make our programs work like other Unix command-line tools.
# 
# ## Download code from Notebook,
# 
# Open Notebook [sieveExample.ipynb](./sieveExample.ipynb)
# and downlad as a python program
# 
# `File` > `Download as` > `Python`

# In[1]:

get_ipython().system(u'cat sieveExample.py')


# ###Run python program 

# In[2]:

get_ipython().magic(u'run sieveExample.py')


# #Python IDE's
# 
# Spyder is a basic IDE coming along Anaconda distribution. It is open-source (google code) and  cross-platform because it's based on Qt library
# 
# Main Features can be found here:
# https://code.google.com/p/spyderlib/wiki/Features
# 
# Documentation can be found here:
# https://pythonhosted.org/spyder/
# 
# 
# 

# In[3]:

#Executing a process in background
#Alternatively, open a new Terminal and type spyder
import os
os.system("spyder &")


# #Command-Line Arguments
# 
# ##How to handle program arguments:  
# `sys.argv` 
# 
# The strange name argv stands for "argument values". Whenever Python runs a program, it takes all of the values given on the command line and puts them in the list sys.argv so that the program can determine what they were. The first element of the list is the name itself of the program. So the first argument is stored in sys.arg[1]
# 
# 

# In the case of sieveExample.py, if we like to pass `n` as argument we should add something like this:
# ```
#    if len(sys.argv)!=2:
#        print 'One Argument is mandatory'
#    else:
#        n = sys.argv[1] 
#        print 'List of primes numbers <', n 
#        print sieveOfEratosthenes(n)
# ```

# However, this code has a flaw: The arguments are **String** types, so a conversion has to be done:
# 
# ```
#    if len(sys.argv)!=2:
#        print 'One Argument is mandatory'
#    else:
#        n = sys.argv[1] 
#        print 'List of primes numbers <', n 
#        print sieveOfEratosthenes(int(n))
# ```

# In[4]:

get_ipython().system(u'cat sieveExampleArgs.py')


# In[6]:

get_ipython().magic(u'run sieveExampleArgs.py 1000')


# As we can import our .py file to a workspace, like any other module,  it is important to enclose the code that is not inside any function in a `main` clause. Thus it will only executed when the file is executed as a script, not when it has been imported.
# 
# ``` if __name__ == '__main__':
#     if len(sys.argv)!=2:
#            print 'One Argument is mandatory'
#     else:
#            n = sys.argv[1] 
#            print 'List of primes numbers <', n 
#            print sieveOfEratosthenes(int(n))
# ```

# In[12]:

import sieveExampleArgs as sea


# Once the module is imported any function can be executed.

# In[13]:

sea.sieveOfEratosthenes(100)


# Indeed it still works as stand alone program:

# In[15]:

get_ipython().magic(u'run sieveExampleArgs 100')


# ##Advanced command-line Arguments
# Argparse module gives functionlities for programming standard command-line behaviours

# In[16]:

get_ipython().system(u'cat sieveExampleArgParse.py')


# In[17]:

get_ipython().magic(u'run sieveExampleArgParse -h')


# In[18]:

get_ipython().magic(u'run sieveExampleArgParse.py 1000')


# In[19]:

get_ipython().magic(u'run sieveExampleArgParse.py -v 1000')


# # Defensive Programming (TESTING)
# 
# Good programing consists in how to tell whether a program is getting the right answer, and how to tell if it's still getting the right answer as we make changes to it.
# 
# To achieve that, we need to:
# 
# * write programs that check their own operation,
# * write and run tests for widely-used functions,
# * make sure we **know** what *correct* actually means.
# 
# 
# ## Basic Rules:
# * A week of hard work can sometimes save you an hour of thought.
# * Fail early, fail often.
# * Turn bugs into assertions or tests.
# * Always initialize from data.
# * Test the simple things first.
# * Know what it's supposed to do.
# * Make it fail every time.
# * Make it fail fast.
# * Change one thing at a time, for a reason.
# * Keep track of what you've done.
# * Be humble.
# 
# 
# ## Assertions
# 
# 
# The first step toward getting the right answers from our programs is to assume that mistakes will happen and to guard against them. This is called defensive programming, and the most common way to do it is to add assertions to our code so that it checks itself as it runs. An assertion is simply a statement that something must be true at a certain point in a program. When Python sees one, it checks that the assertion's condition. If it's true, Python does nothing, but if it's false, Python halts the program immediately and prints the error message provided. 
# 
# For example, this piece of code halts as soon as the loop encounters a value that isn't positive:
# 

# In[20]:

##This code will throws an AssertionError
numbers = [1.5, 2.3, 0.7, -0.001, 4.4]
total = 0.0
for n in numbers:
    assert n >= 0.0, 'Data should only contain positive values'
    total += n
print 'total is:', total


# Programs like the Firefox browser are full of assertions: 10-20% of the code they contain are there to check that the other 80-90% are working correctly. Broadly speaking, assertions fall into three categories:
# 
# * A precondition: is something that must be true at the start of a function in order for it to work correctly.
# * A postcondition: is something that the function guarantees is true when it finishes.
# * An invariant: is something that is always true at a particular point inside a piece of code.
# 
# For example, suppose we are representing rectangles using a tuple of four coordinates `(x0, y0, x1, y1)`. In order to do some calculations, we need to normalize the rectangle so that it is at the origin and 1.0 units long on its longest axis. This function does that, but checks that its input is correctly formatted and that its result makes sense:

# In[22]:

def normalize_rectangle(rect):
    '''Normalizes a rectangle so that it is at the origin and 1.0 units long on its longest axis.'''
    ''' (x0,y0,x1,y1) '''
    assert len(rect) == 4, 'Rectangles must contain 4 coordinates'
    x0, y0, x1, y1 = rect
    assert x0 < x1, 'Invalid X coordinates'
    assert y0 < y1, 'Invalid Y coordinates'
    dx = x1 - x0
    dy = y1 - y0
    if dx > dy:
        scaled = float(dx) / dy
        upper_x, upper_y = 1.0, scaled
    else:
        scaled = float(dx) / dy
        upper_x, upper_y = scaled, 1.0
    assert 0 < upper_x <= 1.0, 'Calculated upper X coordinate invalid'
    assert 0 < upper_y <= 1.0, 'Calculated upper Y coordinate invalid'

    return (0, 0, upper_x, upper_y)


# In[23]:

print normalize_rectangle( (1.0, 2.0, 4.0, 5.0) ) # Correct Rectangle


# In[24]:

##This code will throws an AssertionError
print normalize_rectangle( (0.0, 1.0, 2.0) ) # missing the fourth coordinate


# In[25]:

##This code will throws an AssertionError
print normalize_rectangle( (4.0, 2.0, 1.0, 5.0) ) # X axis inverted


# The post-conditions help us catch bugs by telling us when our calculations cannot have been correct.
# For example, if we normalize a rectangle that is taller than it is wide everything seems OK:

# In[26]:

print normalize_rectangle( (0.0, 0.0, 1.0, 5.0) )


# but if we normalize one that's wider than it is tall, the assertion is triggered:

# In[27]:

##This code will throws an AssertionError
print normalize_rectangle( (0.0, 0.0, 5.0, 1.0) )


# **Why Calculated upper Y coordiate is invalid?**
# 
# This means that y value is not between 0 and 1, as we want.
# Re-reading our function,
# we realize that where it says: 
# 
#     if dx > dy:
#         scaled = float(dx) / dy
# 
# it should divide `dy` by `dx` rather than `dx` by `dy`.

# In[28]:

def normalize_rectangle(rect):
    '''Normalizes a rectangle so that it is at the origin and 1.0 units long on its longest axis.'''
    ''' (x0,y0,x1,y1) '''
    assert len(rect) == 4, 'Rectangles must contain 4 coordinates'
    x0, y0, x1, y1 = rect
    assert x0 < x1, 'Invalid X coordinates'
    assert y0 < y1, 'Invalid Y coordinates'
    dx = x1 - x0
    dy = y1 - y0
    if dx > dy:
        scaled = float(dy) / dx
        upper_x, upper_y = 1.0, scaled
    else:
        scaled = float(dx) / dy
        upper_x, upper_y = scaled, 1.0

    assert 0 < upper_x <= 1.0, 'Calculated upper X coordinate invalid'
    assert 0 < upper_y <= 1.0, 'Calculated upper Y coordinate invalid'

    return (0, 0, upper_x, upper_y)


# If we had left out the assertion at the end of the function,
# we would have created and returned something that had the right shape as a valid answer,
# but wasn't.
# Detecting and debugging that would almost certainly have taken more time in the long run
# than writing the assertion.
# 
# But assertions aren't just about catching errors:
# they also help people understand programs.
# Each assertion gives the person reading the program
# a chance to check (consciously or otherwise)
# that their understanding matches what the code is doing.
# 
# Most good programmers follow two rules when adding assertions to their code.
# The first is, "fail early, fail often". The greater the distance between when and where an error occurs and when it's noticed, the harder the error will be to debug, so good code catches mistakes as early as possible.
# 
# The second rule is, turn bugs into assertions or tests. If you made a mistake in a piece of code,
# the odds are good that you have made other mistakes nearby,
# or will make the same mistake (or a related one)
# the next time you change it.
# Writing assertions to check that you haven't regressed
# (i.e., haven't re-introduced an old problem)
# can save a lot of time in the long run,
# and helps to warn people who are reading the code
# (including your future self) that this bit is tricky.

# Obviously you can catch an AssertionError as any other exception. However this will make that your code stop breaking, which is the opposite idea of assertion!  Assert purpose is to find bugs, try-catch is for handling exceptional situations.

# In[29]:

try: 
    print normalize_rectangle( (4.0, 2.0, 1.0, 5.0) ) # X axis inverted
except AssertionError as e:
    print 'AssertionError', e


# However, in production code, precondition asserts are often substituted by custom exceptions:

# In[30]:

def normalize_rectangle(rect):
    '''Normalizes a rectangle so that it is at the origin and 1.0 units long on its longest axis.'''
    if len(rect) != 4:
        raise Exception('Rectangles must contain 4 coordinates')
    x0, y0, x1, y1 = rect
    if x0 > x1:
        raise Exception('Invalid X coordinates')
    if y0 > y1:
        raise Exception('Invalid Y coordinates')
    dx = x1 - x0
    dy = y1 - y0
    if dx > dy:
        scaled = float(dy) / dx
        upper_x, upper_y = 1.0, scaled
    else:
        scaled = float(dx) / dy
        upper_x, upper_y = scaled, 1.0

    assert 0 < upper_x <= 1.0, 'Calculated upper X coordinate invalid'
    assert 0 < upper_y <= 1.0, 'Calculated upper Y coordinate invalid'

    return (0, 0, upper_x, upper_y)


# In[31]:

print normalize_rectangle( (0.0, 0.0, 5.0, 1.0) )
print normalize_rectangle( (0.0, 0.0, 1.0, 5.0) )
try: 
    print normalize_rectangle( (5.0, 0.0, 1.0, 1.0) )
except Exception as e:
    print e


# ## Debugging

# Once testing has uncovered problems, the next step is to fix them. Many novices do this by making more-or-less random changes to their code until it seems to produce the right answer, but that's very inefficient (and the result is usually only correct for the one case they're testing). The more experienced a programmer is, the more systematically they debug, and most follow some variation on the rules explained below.
# 
# 
# #### Know What It's Supposed to Do
# 
# The first step in debugging something is to know what it's supposed to do 
# "My program doesn't work" isn't good enough: 
# in order to diagnose and fix problems,
# we need to be able to tell correct output from incorrect.
# If we can write a test case for the failing case,
# if we can assert that with *these* inputs,
# the function should produce *that* result,
# then we're ready to start debugging.
# If we can't, then we need to figure out how we're going to know when we've fixed things.
# 
# In practice, data scientists tend to do the following:
# 
# 1.  *Test with simplified data.*
#     Before doing statistics on a real data set,
#     we should try calculating statistics for a single record,
#     for two identical records,
#     for two records whose values are one step apart,
#     or for some other case where we can calculate the right answer by hand.
# 
# 2.  *Compare to an oracle.*
#     A test oracle is something, experimental data,
#     an older program whose results are trusted,
#     or even a human expert, against which we can compare the results of our new program.
#     If we have a test oracle, we should store its output for particular cases
#     so that we can compare it with our new results as often as we like
#     without re-running that program.
# 
# 3.  *Check conservation laws.*
#     Mass, energy, and other quantitites are conserved in physical systems,
#     so they should be in programs as well.
#     Similarly,
#     if we are analyzing patient data,
#     the number of records should either stay the same or decrease
#     as we move from one analysis to the next
#     (since we might throw away outliers or records with missing values).
#     If "new" patients start appearing out of nowhere as we move through our pipeline,
#     it's probably a sign that something is wrong.
# 
# 4.  *Visualize.*
#     Data analysts frequently use simple visualizations to check both
#     the science they're doing
#     and the correctness of their code
#     This should only be used for debugging as a last resort,
#     though,
#     since it's very hard to compare two visualizations automatically.
# 
# #### Make It Fail Every Time
# 
# We can only debug something when it fails,
# so the second step is always to find a test case that
# makes it fail every time.
# The "every time" part is important because
# few things are more frustrating than debugging an intermittent problem:
# if we have to call a function a dozen times to get a single failure,
# the odds are good that we'll scroll past the failure when it actually occurs.
# 
# As part of this, it's always important to check that our code is "plugged in",
# that we're actually exercising the problem that we think we are.
# Every programmer has spent hours chasing a bug,
# only to realize that they were actually calling their code on the wrong data set
# or with the wrong configuration parameters,
# or are using the wrong version of the software entirely.
# 
# Mistakes like these are particularly likely to happen when we're tired,
# frustrated, and up against a deadline,
# which is one of the reasons late-night (or overnight) coding sessions
# are almost never worthwhile.
# 
# #### Make It Fail Fast
# 
# If it takes 20 minutes for the bug to surface,
# we can only do three experiments an hour.
# 
# That doesn't must mean we'll get less data in more time:
# we're also more likely to be distracted by other things as we wait for our program to fail,
# which means the time we *are* spending on the problem is less focused.
# It's therefore critical to make it fail fast.
# 
# As well as making the program fail fast in time,
# we want to make it fail fast in space, this is,
# we want to localize the failure to the smallest possible region of code:
# 
# 1.  The smaller the gap between cause and effect,
#     the easier the connection is to find.
#     Many programmers therefore use a divide and conquer strategy to find bugs,
#     i.e.,
#     if the output of a function is wrong,
#     they check whether things are OK in the middle,
#     then concentrate on either the first or second half,
#     and so on.
# 
# 2.  Every line of code that *isn't* run as part of a test
#     means more than one thing we don't need to worry about.
# 
# #### Change One Thing at a Time, For a Reason
# 
# Replacing random chunks of code is unlikely to do much good.
# (After all,
# if you got it wrong the first time,
# you'll probably get it wrong the second and third as well.)
# Good programmers therefore
# change one thing at a time, for a reason.
# They are either trying to gather more information
# ("is the bug still there if we change the order of the loops?")
# or test a fix
# ("can we make the bug go away by sorting our data before processing it?").
#   
# Every time we make a change,
# however small,
# we should re-run our tests immediately,
# because the more things we change at once,
# the harder it is to know what's responsible for what
# And we should re-run *all* of our tests:
# more than half of fixes made to code introduce (or re-introduce) bugs,
# so re-running all of our tests tells us whether we have re-introduced a bug that was once fixed.
# 
# #### Keep Track of What You've Done
# 
# Good data scientists keep track of what they've done
# so that they can reproduce their work,
# and so that they don't waste time repeating the same experiments
# or running ones whose results won't be interesting.
# Similarly,
# debugging works best when we
# keep track of what we've done
# and how well it worked.
# If we find ourselves asking,
# "Did left followed by right with an odd number of lines cause the crash?
# Or was it right followed by left?
# Or was I using an even number of lines?"
# then it's time to step away from the computer,
# take a deep breath,
# and start working **more systematically**.
#   
# Records are particularly useful when the time comes to ask for help.
# People are more likely to listen to us
# when we can explain clearly what we did,
# and we're better able to give them the information they need to be useful.
# Version Control Systems are often used to reset software to a known state during debugging,
# and to explore recent changes to code that might be responsible for bugs. 
# How to use VCS will be introduced later in this notebook. 
# 
# #### ASK for HELP
# 
# And speaking of help:
# if we can't find a bug in 10 minutes,
# we should  ask for help.
# Just explaining the problem aloud is often useful,
# since hearing what we're thinking helps us spot inconsistencies and hidden assumptions.
# 
# Asking for help also helps alleviate confirmation bias.
# If we have just spent an hour writing a complicated program,
# we want it to work,
# so we're likely to keep telling ourselves why it should,
# rather than searching for the reason it doesn't.
# People who aren't emotionally invested in the code can be more objective,
# which is why they're often able to spot the simple mistakes we have overlooked.
# 
# Programmers tend to get the same things wrong over and over:
# either they don't understand the language and libraries they're working with,
# or their model of how things work is wrong.
# In either case,
# taking note of why the error occurred
# and checking for it next time
# quickly turns into not making the mistake at all.
# And that is what makes us most productive in the long run.
# 
# As the saying goes,
# "A week of hard work can sometimes save you an hour of thought"
# If we train ourselves to avoid making some kinds of mistakes,
# to break our code into modular, testable chunks,
# and to turn every assumption (or mistake) into an assertion,
# it will actually take us *less* time to produce working programs,
# not more.
# 

# #### How to Debug with ipdb debugger:
# 
# There are two ways you can use ipdb for debugging:
# 
# 1- run command with -d param 

# In[50]:

get_ipython().system(u'cat sieveExample.py')


# In[32]:

get_ipython().magic(u'run -d sieveExample.py')


# 1. Set a break point at line 22 using: `b 22` 
# 2. Continue execution to next breakpoint with `c` (ont(inue))
# 3. Type a variable name to see its value: `si`
# 4. Execute next line using: `n`
# 5. Quit debugging session with: `q``
# 
# --- Ask for help using ? followed of command name.
# 

# 2- Using Spyder IDE's (`ctrl`+`F5`)
# 
# * Simple breakpoints can be set from the Run menu, by keyboard shortcut (F12 by default), or by double-click to the left of line numbers in the Editor.
# * Conditional breakpoints can also be set from the Run menu, by keyboard shortcut (Shift+F12 by default), or by Shift+double-click to the left of line numbers in the Editor.
# * Step by step execution can be done using the blue buttons on the tool bar.
# * The current frame (debugging step) is highlighted in the Editor.
# * At each breakpoint, globals may be accessed through the Variable Explorer.
# 
# ?- Use a Conditional Breakpoint to go through the last iteration of the sieve loop.
# 

# ###Key Points
# * Program defensively, i.e., assume that errors are going to arise, and write code to detect them when they do.
# * Put assertions in programs to check their state as they run, and to help readers understand how those programs are supposed to work.
# * Use preconditions to check that the inputs to a function are safe to use.
# * Use postconditions to check that the output from a function is safe to use.
# * Write tests before writing code in order to help determine exactly what that code is supposed to do.
# * Know what code is supposed to do before trying to debug it.
# * Make it fail every time.
# * Make it fail fast.
# * Change one thing at a time, and for a reason.
# * Keep track of what you've done.
# * Be humble.

# ###Challenges
# 
# 1- Write a command-line program that does addition or subtraction or multiply. By default it sums up the two values. Check  `ArgumentParser.add_mutually_exclusive_group()` functionality.
# 
# 
# `python arith.py -a 1 2` / `python arith.py --add 1 2`
# 
# 3
# 
# `python arith.py -s 3 4` / `python arith.py --subtraction 3 4`
# 
# -1
# 
# `python arith.py -m 2 4` /  `python arith.py --multiply 2 4`
# 
# 8
# 
# 2- Write a function called `average` that calculates the average of the numbers in a list.
#    * What pre-conditions and post-conditions would you write for it?
# 

# #Timing

# Now we are sure that our program is correct, we can ask for performance. Given two different algorithms which solves the same problem with the same output, we can say that one gives better performance than the other by comparing its processing times.
# 
# Time function gives us a time mark. It's straightforward to calculate a function processing time by taking marks before and after the function and subtract them.

# In[53]:

import sieveExample
import time
t1 = time.time()
result = sieveExample.sieveOfEratosthenes(100000)
t2 = time.time()
print 'sieveOfEratosthenes took {} seconds'.format(t2 - t1)


# We can also take overall timing of a python script by passing `-t` argument to run command. 
# This print timing information at the end of the run. IPython will give
# you an estimated CPU time consumption and wall clock times for your script. Under Unix, an estimate of time spent on system tasks is also given (for Windows platforms this is reported as 0.0, since it can not be measured). An additional ``-N<N>`` option can be given, where <N> must be an integer indicating how many times you want the script to
# run. The final timing report will include total and per run results.
# 

# In[54]:

get_ipython().magic(u'pinfo %run')
get_ipython().magic(u'run -t -N5 sieveExampleArgParse.py 1000000')


# However if we want more timing with more precision we can use magic command %timeit. 
# 
# **%timeit** executes a function several times, and returns the best time obtained. 
# It will limit the number of runs depending on how long the script takes to execute.
# 
# The number of runs may be set with with -n 1000, for example, which will limit %timeit to a thousand iterations
# 
# The number of rounds %timeit it is executed  can also be modified, using -r. For example -r will produce the best result of 5 executions, by default is 3

# In[56]:

import sieveExample
get_ipython().magic(u'timeit sieveExample.sieveOfEratosthenes(1000000)')


# **Comparing two different implementations**
# 
# Now lets to compare two different implimentations for the same problem. Numpy and scipy both have implemented a method for interpolation function. We can use %timeit to know which function is the fastest one. 

# In[57]:

import numpy as np
import scipy.interpolate as spip 
get_ipython().magic(u'pinfo np.interp')


# In[58]:

get_ipython().magic(u'pinfo spip.interp1d')


# In[61]:

x = np.linspace(0, 2*np.pi, 10)
y = np.sin(x)
xvals = np.linspace(0, 2*np.pi, 50)
#scipy
f = spip.interp1d(x, y)
scipy_vals = f(xvals)
# numpy
numpy_vals = np.interp(xvals, x, y)
#assert if values are close!
assert np.allclose(scipy_vals, numpy_vals) 
#np.allclose?


# Once we have checked that both functions gives us the same result aproximately 
# (absolute(`a` - `b`) <= (`atol` + `rtol` * absolute(`b`)); `rtol`=1e-05, `atol`=1e-08),
# 
# we can check it performance:

# In[62]:

print 'scipy:'
get_ipython().magic(u'timeit -n 10000 -r5 f(xvals)')
print 'numpy:'
get_ipython().magic(u'timeit -n 10000 -r5 np.interp(xvals, x, y)')


# #Profiling

# Now we know the time consumed by an implementation, but this time can be shortened? And the key question how it can be done? First thing is to realize where is consuming more time in our code. Profiling gives us how many time takes each method or function been called. We can see the number of calls, total time, time per call and cummulative time since out function was called.
# 
# At the command line:

# In[63]:

get_ipython().magic(u'run -m cProfile sieveExampleArgs.py 1000000')


# Store profile results and visualize it with [`pstats`](http://docs.python.org/library/profile.html#module-pstats). From command line:

# In[65]:

get_ipython().system(u'python -m cProfile -o sieveExample.prof sieveExampleArgs.py 100000')


# In[66]:

import pstats
stats = pstats.Stats('sieveExample.prof')
stats.print_stats()


# Sorting stats:

# In[67]:

stats.sort_stats('cumtime').print_stats()


# In[68]:

stats.sort_stats('tottime').print_stats(5) #five rows


# In[69]:

stats.sort_stats('cumtime').print_stats(r'range') #filter using Regular Expression 


# We also can use **magic command** %prun for profiling

# In[91]:

get_ipython().magic(u'pinfo %prun')


# In[70]:

import sieveExample
get_ipython().magic(u'prun sieveExample.sieveOfEratosthenes(100000) #Using magic command')


# In[72]:

get_ipython().magic(u'prun -D sieveExample_sieve.prof sieveExample.sieveOfEratosthenes(100000)')


# In[73]:

get_ipython().magic(u'prun -q -D scipy_interp.prof f(xvals)')


# In[74]:

get_ipython().magic(u'prun -q -D numpy_interp.prof np.interp(xvals, x, y)')


# Show stats:

# In[75]:

import pstats
stats = pstats.Stats('scipy_interp.prof')
stats.sort_stats('tottime').print_stats(3) #three rows


# In[76]:

import pstats
stats = pstats.Stats('numpy_interp.prof')
stats.sort_stats('cumtime').print_stats(3) #three rows


# Version Control with Git
# ========================

# Version control also known as Revision control, source control is the
# **management of changes to documents, programs, and other information stored as computer files.**
# 
# They are used in virtually all software development and in all environments, by everyone and everywhere VCS can used on almost any digital content, so it is not only restricted to software development, and is also very useful for manuscript files, figures, data and notebooks!
# 
# Without a VCS, it happens situations like these:

# <img src="http://www.phdcomics.com/comics/archive/phd101212s.gif">
# 
# <img src="http://www.phdcomics.com/comics/archive/phd052810s.gif">
# 
# "Piled Higher and Deeper" by Jorge Cham, http://www.phdcomics.com

# There are two main purposes of RCS systems:
# 
# 1. Keep track of changes in the source code.
#     * Allow reverting back to an older revision if something goes wrong.
#     * Work on several "branches" of the software concurrently.
#     * Tags revisions to keep track of which version of the software that was used for what (for example, "release-1.0")
# 2. Make it possible for serveral people to collaboratively work on the same code base simultaneously.
#     * Allow many authors to make changes to the code.
#     * Clearly communicating and visualizing changes in the code base to everyone involved.

# ###Basic Terminology
# 
# In an VCS, the source code or digital content is stored in a **repository**. 
# 
# * The repository does not only contain the latest version of all files, but the complete history of all changes to the files since they were added to the repository. 
# 
# * A user can **checkout** the repository, and obtain a local working copy of the files. All changes are made to the files in the local working directory, where files can be added, removed and updated. 
# 
# * When a task has been completed, the changes to the local files are **commited** (saved to the repository).
# 
# * If someone else has been making changes to the same files, a **conflict** can occur. In many cases conflicts can be **resolved** automatically by the system, but in some cases we might manually have to **merge** different changes together.
# 
# * It is often useful to create a new **branch** in a repository, or a **fork** or **clone** of an entire repository, when we doing larger experimental development. The main branch in a repository is called often **master** or **trunk**. When work on a branch or fork is completed, it can be merged in to the master branch/repository.
# 
# ### Client-Server VCS
# In Client-Server VCS the **repository** is hosted by a server. A client program is used for managing versions of the local working copy 
# 
# The most important client-server open-source VCS are:
# 
# * CVS  ([Concurrent Version System](http://www.nongnu.org/cvs/))
# * SVN  ([Subversion](http://subversion.apache.org/)) 
# 
# 
# 
# ### Distributed VCS
# In Distrubutd VCS code is shared by different **repositories**. In general, it exists a local repository along the local working copy, and a remote repository for collaborating. 
# 
# With distributed VCS we can **pull** and **push** changesets between different repositories. For example, between the local copy of the repository to a central online reposistory (for example on a community repository host site like github.com).
# 
# The most important distributed open-source VCS are:
# 
# * [Git](http://git-scm.com/)
# * [Mercurial](http://mercurial.selenic.com/)
# 
# 
# <img src="./GitCommands.png">
# 
# 

# ##Working with a distant repository 
# 
# With a hosted repository it easy to collaborate with colleagues on the same code base, and you get a graphical user interface where you can browse the code and look at commit logs, track issues etc.
# 
# Some good hosted repositories are
# 
# * [Github](http://www.github.com)
# * [Bitbucket](http://www.bitbucket.org)
# 
# Github.com is a web hosting plateform for git projects. It provide free git repository for opensource projects (private ones can be purchased, or asked for free for [students](https://education.github.com/discount_requests/new)) as well as it provides great tools to review code, manage projects, release packages and publish documentation. Most of the scientific python code you will use in this course are hosted on github.
# 
# Bitbucket.com provides unlimited private code repositories for free for teams up to 5 developers
# 
# There are also a number of graphical users interfaces for GIT. The available options vary a little bit from platform to platform:
# 
# * http://git-scm.com/downloads/guis

# Now, let’s go on github.com, and create an account:
# 
# https://github.com/join

# Once this is done, we can easily create a new project by cliking on the green button, on the main page:

# https://github.com/new
# 
# Github redirects you to a page, where you specify the name of the repository and a few information. By default, git repositories hosted on github will be public. 
# Github then displays a page with a url, and some information on how to proceed to configure your local repository. Note that if you decide to create a README file, a Licence or a .gitignore on github, it will automatically commit.

# **Hands On**
# 
# Create a Repository called `DataScience` in your github account

# First, we have to **clone** the remote repository.
# The name of the repository can be found at the right part of the screen:
# 
# <img src="./GitHub.png">
# 
# 
# You can **clone** the repository through you Github Desktop client by clicking in button `Clone in Desktop`
# 
# Next, your Github Desktop will open. You will be asked for what directory you want to clone the repository. Then the Github Desktop will open. 
# 
# From now on, all changes to this repository will be shown in the `Changes` tab. 

# **Hands On**
# Download your notebook exercices as .py file. Put your code in a directory called `DataScience-exercices` inside your `DataScience` repository 

# Now you can observe that exists changes in your local copy. The first thing to do, is add this document to the Repository. In your Desktop client it would by tagged as New. Now write a comment on the `Summary` text area  and commit the changes to your **Local** repository. This can be done by pressing the `commit` button

# The changes have not been upload to remote repostitory yet. If you check your repository on github.com, you'll see that the changes are not present. To do this you need to `push` your changes. 
# 
# **Hands On**
# 
# In the menu `Repository` select `Push` option. Now the changes are published to the remote repository
# 
# If you remove any file in your local directory, it will be marked as deleted

# ###Collaborating

# **Hands On**
# 
# Now we're going to form teams of 5 students. Choose one github user of your team for work with. 
# Go to `Settings` [page](https://github.com/eloipuertas/ES2013Dimarts/settings) and add your other team members. 
# 
# Now follow the next steps:
# * Clone your team user `DataScience` Repository
# * Go to `DataScience-exercices` file and execute it.
# * Create a new commentary on the beggining of the file with your avaluations and comments about the first excercise
# * Commit changes.
# * Push changes.
# 
# It have ocurred any **conflict**?
# If it does, resolve them:
# * Revise `history` tab to see the different updates of the repository.
# 
# 
# 
# 
# Finally `Pull` the repository to update the changes in your local repositories. (In the menu `Repository` select `Pull` option)
# 
# 
# 
# Now do the same thing but using the notebook file instead of the python file. Upload your version of notebook, and the rest of the group change it, putting news cells with comments and avalauation.
# 
# * It have ocurred any **conflict**? If it does, resolve them.
# 
# Now you can see how looks like your notebook in the nbviewer webpage:
# 
# http://nbviewer.ipython.org/
# 
# Just put your username and repository

# ##Working with a local repository
# 

# You can create a local repository in your machine instead of using a distant repository.
# In the GitHub Desktop client press the `+` symbol and go to the `Create` tab. It ask you for a repository name and the local path. Once create it you can commit new versions.

# **Hands On**
# 
# * create a new git local repository called gitdemo
# 
# * Add your notebook files.
# 
# * Commit them
# 
# * Push them 

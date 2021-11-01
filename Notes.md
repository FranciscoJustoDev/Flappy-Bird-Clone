
# **FlappyBirdClone** - General Guidelines

This is a game about a flying bird or weird creature!

> ## ***To Do:***
> 
> - add Sfx and music!  
> - add **Main Menu** and **Game Over Menu**.  
> - randomly generate `OBSTACLE_GAP` according to
> player size and jump_force.  
> - adjust gravity, jump force and obstacle
> speed values!.  
> - player `jump_force` <= `obstacle_gap`
> **minimum** size! (so that player can move
> pass the obstacle!)  
> - implement art for obstacles and
> background.  
> - add score counter based on number of
> obstacles cleared and highscore from
> playing session.  

> ## ***To Fix:***
>
> - player collider is rect when player image
> is a circle.  
> - *Obstacle stretching* when reaching left
> side of screen.  
> - on `quit()` shell errors like: video sys no
> initialized.  

> ### ***ADDED:***
>
> - added art for player when *idle*, jumping
> and dead.  
> - add jump animation when player dies and wait
> for it to finish before reset.  
> - game now resets when player collides with
> obstacle or goes out of bounds.
> - add collision detection between player and
> obstacles. 
> - add wait time before applying gravity on
> player at startup of game!  
> - obstacles now appear in both ends of
> screen!  
> - delay between jumps  
> - separate groups for player and obstacles  
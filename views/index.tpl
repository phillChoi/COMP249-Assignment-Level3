% rebase('base.tpl')
% import interface


<h2>{{title}}</h2>

%if session_user is None:
<div class="loginform">
    <form method="POST" action="/login" id="loginform">
        <fieldset>
            <legend>Login Form</legend>
            <ul>
                <li>Username: <input name="nick">
                </li>
                <li>Password <input name="password">
                </li>
            <ul><input type='submit' value='Login'>
        </fieldset>
    </form>
</div>

% else:
<div class="log">
    <form id="logoutform" action="/logout" method="POST">
        <p>Logged in as {{session_user}}</p>
        <input type="submit" value="logout">
    </form>
</div>
<div class="postform">
    <form method="POST" action="/post" id="postform">
        <fieldset>
            <textarea name="post" rows="5" cols="50" width="auto"></textarea>
            <input type="submit" value="submit">
        </fieldset>
    </form>
</div>

%end


<div class="posts">

% for post in posts:
       <div class="post">
           <div class="avatar"><img src="{{post[3]}}" alt="avatar"></div>
           <a class="user" href="/users/{{post[2]}}">@{{post[2]}}:</a>
           <span class="timestamp">{{post[1]}}</span> <span class="content">{{!interface.post_to_html(post[4])}}</span>
       </div>
    % end

</div>
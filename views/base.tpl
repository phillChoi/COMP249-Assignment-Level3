<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>{{title}}</title>

    <!-- Custom styles for this template -->
    <link href="/static/psst.css" rel="stylesheet">
  </head>

  <body>

    <ul class="nav navbar-nav">
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>


    <div class="container">
    %if session_user:
    <form id="logoutform" action="/logout" method="POST">
        <input type="submit" value="logout">
    </form>
    %end

		{{!base}}

    </div>

  </body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Inventory Management System</title>
  <link rel="icon" href="<%=request.getContextPath()%>/images/favicon.ico"> 
  <link href="<%=request.getContextPath() %>/css/bootstrap.min.css" rel="stylesheet">
  <link href="<%=request.getContextPath() %>/font-awesome/css/font-awesome.min.css" rel="stylesheet">
  <link href="<%=request.getContextPath() %>/css/styles.css" rel="stylesheet">
  <!--[if lt IE 9]>
 	  <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
 	  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
  <![endif]-->
  <script src="<%=request.getContextPath()%>/js/jquery-1.10.2.js"></script>
   <script type="text/javascript" src="<%=request.getContextPath() %>/js/jquery.min.js"></script>
  <script type="text/javascript" src="<%=request.getContextPath() %>/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="<%=request.getContextPath()%>/js/jquery.dataTables.min.js"></script>
  <script type="text/javascript" src="<%=request.getContextPath()%>/js/dataTables.bootstrap.min.js"></script>
  <script type="text/javascript" src="<%=request.getContextPath() %>/js/metisMenu.min.js"></script>
  <script type="text/javascript" src="<%=request.getContextPath() %>/js/sb-admin-2.js"></script>
  <script type="text/javascript" src="<%=request.getContextPath() %>/js/jquery.blockUI.js"></script>
  <script type="text/javascript" src="<%=request.getContextPath() %>/js/jquery.numeric.js"></script>
  <script type="text/javascript" src="<%=request.getContextPath()%>/js/JqueryAjaxFormSubmit.js"></script>
  <script type="text/javascript" src="<%=request.getContextPath()%>/js/jquery.form.js"></script>
  <script type="text/javascript" src="<%=request.getContextPath()%>/js/jquery.scrollintoview.min.js"></script>
  <script type="text/javascript" src="<%=request.getContextPath() %>/js/commonUtil.js"></script>
  <script src="<%=request.getContextPath() %>/js/raphael-min.js"></script>
  <script src="<%=request.getContextPath() %>/js/morris.min.js"></script>
  
  
<script type="text/javascript">
var context = "<%=request.getContextPath()%>";
	function check(){
 setCookie();  

}
$("[href]").click(function(){
   setCookie();

});
function Delete_Cookie(name) {
	var cookies = document.cookie.split(";");	
	for (var i = 0; i < cookies.length; i++)
	 {
	 	x=cookies[i].substr(0,cookies[i].indexOf("="));
			 x=x.replace(/^\s+|\s+$/g,"");
	 	if(x==name)
	 	{
	 	document.cookie = name + "=" +";expires=Thu, 01-Jan-1970 00:00:01 GMT";
	 	}		 	
	 }
}

function getCookie(c_name)
{
var i,x,ARRcookies=document.cookie.split(";");
for (i=0;i<ARRcookies.length;i++)
{
  x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
 
  x=x.replace(/^\s+|\s+$/g,"");
  if (x==c_name)
    {
    return true;
    }
  }
  return false;
}

function setCookie()
{               
  if(getCookie("clicked")==false) 
  {
  	document.cookie='clicked=1';
  }   
}

window.onload= function()
{		
             	       
  //alert(document.cookie);
  //alert(getCookie("clicked"));   
   if(getCookie("clicked")==false && window.location.href !="<%=request.getContextPath()%>")
   {
	window.history.forward();
   }
   Delete_Cookie("clicked");
};
  <%
  		String msg = null;
  		if(request.getAttribute("message") != null)
  			msg = (String) request.getAttribute("message");
  %>

  	var msg = "<%=msg%>";
	$(document).ready(function()
	{
		if(msg == "failure")
		{
	    	 $('#errorMsg').html("Invalid login credentials");
	    	 $('#errorMsg').show();
	    	 setTimeout('hideStatus("errorMsg")',5000);
		}
		else if(msg == "NOT_ACTIVE")
		{
			$('#errorMsg').html("Login Failed, you have been BLOCKED from the system, please contact the administrator");
	    	$('#errorMsg').show();
	    	setTimeout('hideStatus("errorMsg")',5000);
		}
	});

	function forgotPassword()
	{
		var url = "<%=request.getContextPath()%>/redirect.html?q=forgot_password";
		window.location = url;
	}
	function openDownloadsForms()
	{
		var url = "<%=request.getContextPath()%>/pages/common/downloadForms.jsp";
		window.location = url;
	}
	function openCircular() {
		window.open(context+"/HardCopyForms/Circular.pdf",'','width=700,height=900');
	 }	
  </script>
</head>
<body>
 <form action="<%=request.getContextPath()%>/Login" method="post" onsubmit="check()">
 	<div class="container">
		<header>
		<div class="row">
	     <div class="col-md-5" align="right">
	     <img src="<%=request.getContextPath()%>/images/aims_header.png" class="img-responsive"   alt="Cinque Terre">
	     </div>
	     <div class="col-md-7" align="left">
	     <img src="<%=request.getContextPath()%>/images/aims3.png" class="img-responsive"   alt="Cinque Terre">
	     <!--<h1>
				Government-Wide Assets Inventory Management System
			</h1>
	     -->
	     </div>
	    </div>
	    </header>
	    <!--<div class="row">
	     <div class="col-md-1" align="right"></div>
	     <div class="col-md-11" >
	     <font color="Green"><b>Notification :</b> Circular for registration of Pool Vehicle in the Asset Inventory Management System. <b><a href="#Download" onclick = "openCircular();">Click Here to Download.</a></b></font>
	     </div>
	     </div>
	   -->
	   <div class="row">
	     <div class="col-md-1" align="right"></div>
	     <div class="col-md-11" align="center">
	     <font color="Green"><b><a href="#" onclick="openDownloadsForms()"><i class='fa fa-cloud-download fa-fw'></i> Download Forms</a></b></font>
	     </div>
	     </div>
	   <div class="row">
	    <div class="col-md-6" align="center">
	    <br>
	     <img src="<%=request.getContextPath()%>/images/Fixed-Assets.jpg" class="img-responsive" alt="Cinque Terre"> 
	    </div>
	      <div class="col-md-4" >
	      <br><br><br>
	      <div class="panel panel-default">
		     		<div class="panel-heading ">
		     			<i class="fa fa-gears fa-fw"></i> <strong>Login into your account</strong>
		     		</div>
		     		<div class="panel-body">
		     			<div class="alert alert-danger" id="errorMsg" style="display:none"></div>
		     			<div class="input-group">
					      <div class="input-group-addon"><i class="fa fa-user fa-fw"></i></div>
					      <input type="text" class="form-control" id="loginId" name="loginId" placeholder="Login ID" required autofocus tabindex="1">
					    </div>
					    <br>
					    <div class="input-group">
					      <div class="input-group-addon"><i class="fa fa-lock fa-fw"></i></div>
					      <input type="password" class="form-control" id="password" name="password" placeholder="Password" required autofocus tabindex="2">
					    </div>
		     		</div>
		     		<div class="panel-footer">
		     		<button class="btn btn-primary" id="btn-1" tabindex="3" value="Login" >Login</button>
		     			<!--<input type="submit" class="btn btn-primary" id="Button" tabindex="3" value="Login">
		     			--><div class="pull-right">
		     				<a href="#" onclick="forgotPassword()">Forgot Password?</a>
		     			</div>
		     		</div>
		     	</div> <!-- /panel -->
	    </div>
	    <div class="col-md-2 ">
	    </div>
	    </div>
	    
 		<footer>
 	
            <h1>
            	<span>
            		&copy; Copyright 2015, Department of National Properties, Ministry of Finance
            	</span>
            </h1>
        </footer>
        	
        
        <!--
        <div class="panel panel-default">
        	<div class="panel-heading">
        		<i class="fa fa-th-list fa-fw"></i> Links
        	</div>
        	<ul class="list-group">
      			<li class="list-group-item">
      				<a href="<%=request.getContextPath()%>/admin.html?method=addToLdapUser"><span>Add to ldap</span></a><br>
      				
      			   	<a href="<%=request.getContextPath()%>/MasterScreen.html?method=parentMasterDtls"><span>Primary Master Screen</span></a><br>
      			   	<a href="<%=request.getContextPath()%>/MasterScreen.html?method=agencyMasterDtls"><span>Agency Master Screen</span></a><br>
      			   	<a href="<%=request.getContextPath()%>/MasterScreen.html?method=subAgencyMasterDtls"><span>Sub Agency Master Screen</span></a>
					<a href="<%=request.getContextPath()%>/MasterScreen.html?method=parentMasterDtls"><span>Primary </span></a><br>
      			   	<a href="<%=request.getContextPath()%>/MasterScreen.html?method=agencyMasterDtls"><span>Agency</span></a><br>
      			   	<a href="<%=request.getContextPath()%>/MasterScreen.html?method=subAgencyMasterDtls"><span>Sub Agency </span></a><br>
      			    <a href="<%=request.getContextPath()%>/MasterScreen.html?method=assetTypeMasterDtls"><span>Asset Group</span></a><br>
      			    <a href="<%=request.getContextPath()%>/MasterScreen.html?method=assetTypeItemMasterDtls"><span>Asset Group Item </span></a><br>
      			    <a href="<%=request.getContextPath()%>/MasterScreen.html?method=assetManufactureMasterDtls"><span>Asset Manufacturer </span></a><br>
      			    <a href="<%=request.getContextPath()%>/MasterScreen.html?method=assetModelDtls"><span>Asset Model </span></a><br>
      				<a href="<%=request.getContextPath()%>/MasterScreen.html?method=assetDisposalTypeDtls"><span>Disposal Type </span></a><br>
      				<a href="<%=request.getContextPath()%>/MasterScreen.html?method=assetAcquisitionTypeDtls"><span>Acquisition Type </span></a><br>
      				<a href="<%=request.getContextPath()%>/MasterScreen.html?method=assetMaintenenceDtls"><span>Maintainance Type </span></a><br>
      				<a href="<%=request.getContextPath()%>/MasterScreen.html?method=titleDtls"><span>Title Type </span></a><br>
      			   	<p><a href="<%=request.getContextPath()%>/pages/building/allocation.jsp"><span>Allocation</span></a></p>
      			    <a href="<%=request.getContextPath()%>/MasterScreen.html?method=assetManufactureMasterDtls"><span>Asset Manufacturer </span></a><br>
      			   	<a href="<%=request.getContextPath()%>/MasterScreen.html?method=assetModelDtls"><span>Asset Model </span></a><br>
      				<a href="<%=request.getContextPath()%>/MasterScreen.html?method=assetDisposalTypeDtls"><span>Disposal Type </span></a><br>
      				<a href="<%=request.getContextPath()%>/MasterScreen.html?method=assetAcquisitionTypeDtls"><span>Acquisition Type </span></a><br>
      				<a href="<%=request.getContextPath()%>/MasterScreen.html?method=assetMaintenenceDtls"><span>Maintainance Type </span></a><br>
      				<a href="<%=request.getContextPath()%>/MasterScreen.html?method=titleDtls"><span>Title Type </span></a><br>
      			<a href="<%=request.getContextPath()%>/MasterScreen.html?method=titleDtls"><span>Title Type </span></a><br>
      			</li>
           	</ul>
        </div>
    -->
    </div> <!-- /container -->
  </form>
</body>
</html>
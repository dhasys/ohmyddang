function get_prefix_data(type){
	var result;
	var prefix_store_data;
	var prefix_coupon_data;

	prefix_coupon_data = {
		'coupon_name':'쿠폰명을',
		'description':'쿠폰소개글을'
		// 'original_price' : '판매원가를'
	};

	prefix_store_data = {
		'store_name':'가맹점명을',
		'president_name':'대표자명을',
		'business_number':'사업자등록번호를',
		'id':'아이디를',
		'dayoff':'휴무일을',
		'manager_name':'담당자를',
		'manager_phone':'당담자연락처를',
		'address_detail':'주소를'
	};

	prefix_member_data = {
		'member_id':'id를',
		'member_nickname':'닉네임을',
		'business_number':'사업자등록번호를'
	};

	if(type == 'coupon'){
		result = prefix_coupon_data;
	}else if(type == 'store'){
		result = prefix_store_data;
	}else if(type == 'member'){
		result = prefix_member_data;
	}
	return result;
}

function validate_board_register(){
	var title = $("#board_title").val();
	var contents = $("#board_contents").val();
	if(title===""){
		alert("제목을 입력해주세요");
		return false;
	}else if(contents===""){
		alert("내용을 입력해주세요");
		return false;
	}
	return true;
}

function validate_board_reply_register(){
	var contents = $("#reply_contents").val();	
	if(contents===""){
		alert("내용을 입력해주세요");
		return false;
	}
	return true;
}

function validate_notice_register(){
	var title = $("#notice_title").val();
	var contents = $("#notice_contents").val();
	if(title===""){
		alert("제목을 입력해주세요");
		return false;
	}else if(contents===""){
		alert("내용을 입력해주세요");
		return false;
	}
	return true;
}

function validate_push_register(){
	var contents = $("#push_contents").val();
	if(contents===""){
		alert("내용을 입력해주세요");
		return false;
	}

	if($("#time_type1").attr("checked")=="checked"){
		if(!validate_date($("#start_y").val() + $("#start_m").val() + $("#start_d").val())){
			alert('유효하지 날짜를 입력하셨습니다');
			return false;
		}
		var today = new Date();
		var year = today.getFullYear();
		var month = today.getMonth() + 1;
		var day = today.getDate();
		var hour = today.getHours();
		var monutes = today.getMinutes();
		var today_text = String(year) + String(month) + String(day) + String(hour) + String(monutes);

		var push_date = $('#start_y').val();
		push_date += $('#start_m').val();
		push_date += $('#start_d').val();
		push_date += $('#start_h').val();
		push_date += $('#start_minute').val();

		if(parseInt(push_date) < parseInt(today_text)){
			alert('오늘날짜보다 큰 날짜를 입력해주세요.');
			return false;
		}
	}
	return true;
}

function validate_review_register(){
	var review_member_name = $("#review_member_name").val();
	var contents = $("#review_contents").val();
	
	if(review_member_name===""){
		alert("작성자를 입력해주세요");
		return false;
	}

	if(contents===""){
		alert("내용을 입력해주세요");
		return false;
	}
	return true;
}

function validate_point_register(){
	var point = $("#point").val();
	var price = $("#price").val();
	
	if(price===""){
		alert("가격을 입력해주세요.");
		return false;
	}

	if(point===""){
		alert("제공포인트 또는 제공기간을 입력해주세요");
		return false;
	}

	if(!check_number("#price", " 가격은")){
		return false;
	}

	if(!check_number("#point", " 제공포인트/ 제공기간은 ")){
		return false;
	}

	return true;
}

function validate_store_register(){
    var is_validate = true;
	var obj = $("#register_form input:text");
	var mode = 'register';
	
	if($("#s_id").val() > 0)	mode = "modify";

	is_validate = check_empty_blank(get_prefix_data('store'), obj);

	if(!is_validate){
		return false;
	}

	var email = $('#register_form input:text[name=email]').val();

	if(mode=="register"){
		//var number = $('#business_number').val();
		//if(!validate_business_number(number)){
		//	alert("올바른 사업자 등록번호를 입력해주세요");
		//	return false;
		//}

		if(!validate_store_id_email()){
			return false;
		}

		if(!check_id_character()){
			return false;
		}

		var assent_check = $('#register_form input:checkbox[name=chk_validate]');
		if (!assent_check[0].checked) {
			alert('이용약관에 동의해주세요.');
			return false;
		}

		var personal_info_check = $('#register_form input:checkbox[name=chk_personal_info]');
		if (!personal_info_check[0].checked) {
			alert('개인정보취급방침에 동의해주세요');
			return false;
		}
	}

	if(!validate_password()){
		// alert("비밀번호가 일치하지 않습니다.");
		return false;
	}

	if(!check_phone_number()){
		return false;	
	}

	if(!validateEmail(email)){
		alert('올바른 e-mail 을 입력해 주세요');
		return false;
	}


	if(!validate_worktime()){
		alert("올바른 영업시간을 입력하세요");
		return false;
	}

	if($('#register_form input:text[name=address]').val().length==0){
		alert('올바른 주소를 입력해 주세요');
		return false;
		}

	if($("#lat").val().length==0||$("#lng").val().length==0){
		return true;
		alert('위치보기 버튼을 이용하여 매장의 정확한 위치를 입력해 주시기 바랍니다.');
		return false;
	}

	return true;
}


function check_phone_number(){
	var result = true;
	var num = $('#register_form input:text[name=manager_phone]').val();
	var pattern = /([^0-9])/;
	if(pattern.test(num)){
		alert("전화번호는 숫자만 허용합니다.");
		result = false;
	}
	return result;
 }

 function check_number(element, msg){
	var result = true;
	num = $(element).val();
	var pattern = /([^0-9])/;
	if(pattern.test(num)){
		alert(msg + "숫자만 허용합니다.");
		result = false;
	}
	return result;
 }

function check_id_character(){
	var result = true;
	var alph = $('#register_form input:text[name=store_id]').val();
	var pattern = /[^(a-zA-Z0-9)]/;
	if(pattern.test(alph)){
		alert("이름은 영문과 숫자만 허용합니다.");
		result = false;
	}
	return result;
 }

function validateEmail(email){
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function validate_store_id_email(){
	var result = true;
	var id = $('#register_form input:text[name=store_id]').val();
	var email = $('#register_form input:text[name=email]').val();
	$.ajax({
		type: 'GET',
		url: '/api/s/idcheck?id=' + id +'&email=' + email,
		dataType: 'text',
		success: function(data){
			if(data!='성공'){
				alert(data);
				result = false;
			}
		},
		async: false
	});
	return result;
}

function validate_member_register(){
var is_validate = true;
	var obj = $("#member_register_form input:text");
	var bir_year = $("#birth_year").val();
	var bir_mon = $("#birth_month").val();
	var bir_day = $("#birth_day").val();
	var today = new Date();
  	var today = new Date();
	var year = today.getFullYear();
	var month = today.getMonth() + 1;
	var day = today.getDate();
	var today_text = String(year) + String(month) + String(day);
	var birth_text = String(bir_year) + String(bir_mon) + String(bir_day);

	is_validate = check_empty_blank(get_prefix_data('member'), obj);

	if(!is_validate){
		return false;
	}

	if(!validate_member()){
		return false;
	}

	if(!validate_date($("#birth_year").val() + $("#birth_month").val() + $("#birth_day").val())){
			alert('유효하지 않은 생일을 입력하셨습니다');
			return false;
	  }

	if(parseInt(birth_text) > parseInt(today_text)){
		alert('유효하지 않은 생일을 입력하셨습니다.');
		return false;
	}
	if(!check_number("#member_coupon_down_count", "쿠폰다운수는 ")){
		return false;
	}

	if(!check_number("#member_coupon_use_count", "쿠폰사용수는 ")){
		return false;
	}
	return true;
}

function validate_member(){
	var result = true;
	var member_id = $('#member_register_form input:text[name=member_id]').val();
	var member_nickname = $('#member_register_form input:text[name=member_nickname]').val();
	$.ajax({
		type: 'GET',
		url: '/api/c/member/register?member_id=' + member_id + '&member_nickname=' + member_nickname + '&isResponse=true',
		dataType: 'text',
		success: function(data){
			if(data=='id'){
				alert('중복된 id 입니다. 다시입력해주세요');
				result = false;
			}else if(data=='nick'){
				alert('중복된 닉네임 입니다. 다시입력해주세요');
				result = false;
			}
		},
		async: false
	});
	return result;
}

function get_prefix_data(type){
	var result;
	var prefix_store_data;
	var prefix_coupon_data;
	var prefix_member_data;

	prefix_coupon_data = {
		'coupon_name':'쿠폰명을',
		'coupon_count' : '쿠폰개수를'
	};

	prefix_store_data = {
		'store_name':'가맹점을',
		'president_name':'대표자명을',
		'business_number':'사업자등록번호를',
		'id':'아이디를',
		'email':'이메일을',
		'manager_name':'담당자를',
		'manager_phone':'당담자연락처를',
		'address_detail':'주소를'
	};

	prefix_member_data = {
		'member_id':'ID를',
		'member_nickname':'닉네임을',
		'member_coupon_down_count': '쿠폰다운수를',
		'member_coupon_use_count': '쿠폰사용수를'
	};

	if(type == 'coupon'){
		result = prefix_coupon_data;
	}else if(type == 'store'){
		result = prefix_store_data;
	}else if(type == 'member'){
		result = prefix_member_data;
	}
	return result;
}

function check_empty_blank(data, form_id){
	var obj = form_id;
	var is_validate = true;
	obj.each(function(i, v){
		if(this.value.length === 0 && is_validate === true){
			if(data[this.name]!=undefined){
				var text = this.name;
				is_validate = false;
				alert(data[text] + "채우세요.");
				return; 
			}
		}
	});

	if(!is_validate){
		return false;
	}
	return true;
}

function validate_business_number(business_num)  
{
	return true;
	
	//사업자등록번호 체크  
    // business_num는 숫자만 10자리로 해서 문자열로 넘긴다. 
    var checkID = new Array(1, 3, 7, 1, 3, 7, 1, 3, 5, 1); 
    var tmpBizID, i, chkSum=0, c2, remander; 
     business_num = business_num.replace(/-/gi,''); 

     for (i=0; i<=7; i++) chkSum += checkID[i] * business_num.charAt(i); 
     c2 = "0" + (checkID[8] * business_num.charAt(8)); 
     c2 = c2.substring(c2.length - 2, c2.length); 
     chkSum += Math.floor(c2.charAt(0)) + Math.floor(c2.charAt(1)); 
     remander = (10 - (chkSum % 10)) % 10 ; 

    if (Math.floor(business_num.charAt(9)) == remander) return true ; // OK! 
      return false; 
} 

function validate_worktime(){
	var worktime = $('#register_form select');
	var open = worktime[0].value + worktime[1].value;
	var close = worktime[2].value + worktime[3].value;
	if(open==close || open>close){
		return false;
	}
	return true;
}

function validate_password(){
	var pass1 = $('#register_form input:password[name=password]').val();
	var pass2 = $('#register_form input:password[name=password_validation]').val();

	if(pass1.length < 4 || pass2.length < 4 ){
		alert('비밀번호 4 자리 이상을 입력해주세요');
		return false;
	}else{
		if(pass1 == pass2){
			return true;
		}else{
			alert('비밀번호가 일치하지 않습니다.');
			return false;
		}
	}
}

function get_geo(){
	var str = $('#register_form input:text[name=address]').val();
	var lat = 0;
	var lng = 0;
	var result = true;

	$.ajax({
		type: 'GET',
		url: '/api/s/geo?address=' + str,
		dataType: 'json',
		success: function(data){
			if(data['results'].length == 1){
				lat = data['results'][0]['geometry']['location']['lat'];
				lng = data['results'][0]['geometry']['location']['lng'];
				$('#register_form input:hidden[name=lat]').val(lat);
				$('#register_form input:hidden[name=lng]').val(lng);
			}else{
				result = false;
			}
		},
		async: false
	});
	return result;
}

function validate_coupon_register(){
	var is_validate = true;
	var obj = $("#coupon_register_form input:text");
	var discount_type = $(':radio[name="discount_type"]:checked').val();
	is_validate = check_empty_blank(get_prefix_data('coupon'), obj);
	
	if(!is_validate){
		return false;
	}

	if(!check_number("#coupon_count", "쿠폰개수는")){
		return false;
	}

	if(discount_type == "0"){
		// 가격기준
		if(!check_number("#original_price", "판매원가는")){
			return false;
		}

		if($('#original_price').val() == ""){
			alert('판매원가를 입력하세요');
			return false;
		}

		if(!check_number("#discount_price", "할인가는")){
			return false;
		}	

		if($('#discount_price').val()== ""){
			alert('할인가를 입력하세요');
			return false;
		}

	}else if(discount_type == "1"){
		// 할인율기준
		if(!check_number("#discount_percentage", "할인율은")){
			return false;
		}else{
			if($('#discount_percentage').val()==0){
				alert('0 이상의 할인율을 입력해주세요');
				return false;
			}
		}
	}

	if(!coupon_count_check()){
		return false;
	}

	return true;
}

function coupon_count_check(){
	count = $('#coupon_count').val();
	s_id = $('#store_id').val();
	c_id = $('#c_id').val();
	if(count==0){
		alert('쿠폰개수를 입력해주세요');
		return false;
	}
	$.ajax({
		type: 'GET',
		url: '/api/s/coupon/point?s_id=' + s_id +'&count=' + count + '&c_id=' + c_id ,
		dataType: 'text',
		success: function(data){
			if(data==0){
				alert('잔여포인트가 없습니다. 포인트를 구매후 쿠폰등록 가능합니다.');
				result = false;
			}else if(data=='정액제'){
				alert('정액제 상품 이용중입니다.쿠폰 등록이 가능합니다.');
				result = true;
			}else if(data=='성공'){
				alert('잔여포인트가 있습니다. 쿠폰등록이 가능합니다.');
				result = true;
			}else{
				alert('error');
				result = false;
			}
		},
		async: false
	});

	return result;
}

function validate_date(date){
	if(date.length!=8){
		return false;
	}

	o_date = new Date();
	o_date.setFullYear(date.substring(0, 4));
	o_date.setMonth(parseInt(date.substring(4, 6))-1);
	o_date.setDate(date.substring(6));
	if(o_date.getFullYear()!=date.substring(0,4)
			||o_date.getMonth()+1!=date.substring(4, 6)
			||o_date.getDate()!=date.substring(6)){
		return false;
	}

	return true;
}

function store_logout_check(){
	if(confirm("관리자로 로그인 하시겠습니까?")){
		location.href = "/store/login/0";
  	}  
}

function point_type_change(value){    
	if(value==1){
   		$("#point_text").text('p');
	}else if(value==2){      
  		$("#point_text").text('일');
	}
}

function point_delete(id){
	if(confirm('삭제하시겠습니까?')){
		location.href = "/delete/point/" + id;
	}
}

function cert_status(code,dom)
{
	// 인증마크.
    var urlname = "http://sgssl.net/cgi-bin/cert-seal4?code="+ code + "&dom="+ dom;
    window.open(urlname, "cert_status","height=600,width=550, menubar=no,directories=no,resizable=no,status=no,scrollbars=yes");
    return;
}

function info_popup()
{
    var urlname = "/popup/info";
    window.open(urlname, "info_popup","height=600,width=550, menubar=no,directories=no,resizable=no,status=no,scrollbars=yes");
    return;
}

function start_popup()
{
    var urlname = "/popup/start";
    window.open(urlname, "start_popup","height=600,width=550, menubar=no,directories=no,resizable=no,status=no,scrollbars=yes");
    return;
}

function assent_popup()
{
    var urlname = "/popup/assent";
    window.open(urlname, "assent_popup","height=600,width=550, menubar=no,directories=no,resizable=no,status=no,scrollbars=yes");
    return;
}

$(document).ready(function(){
	// 가맹점 회원가입시 가입요청 버튼 눌렸을 경우 동작하도록 설정
	if($('#register_form').length>0){
		$('#register_form').submit(validate_store_register);
		$('#certification').click(function(){
			var num = $('#business_number').val();
			if(num == ""){
				alert('사업자 등록번호를 입력해주세요');
			}else{
				if(!validate_business_number(num)){
					alert('올바른 사업자 등록번호를 입력해주세요');
				}else{
					alert('사업자 등록번호가 인증되었습니다.');
			}
			}			
		});
	}   

	if($('#member_register_form').length>0){
		$('#member_register_form').submit(validate_member_register);
	}

	if($('#notice_register_form').length>0){
		$('#notice_register_form').submit(validate_notice_register);
	}

	if($('#push_register_form').length>0){
		$('#push_register_form').submit(validate_push_register);
	}

	if($('#board_register_form').length>0){
		$('#board_register_form').submit(validate_board_register);
	}

	if($('#board_reply_register_form').length>0){
		$('#board_reply_register_form').submit(validate_board_reply_register);
	}

	if($('#review_register_form').length>0){
		$('#review_register_form').submit(validate_review_register);
	}

	if($('#months.on').length>0){
		$('.innergraph1').removeClass('innergraph1').addClass('innergraph2');
		$('.graph1').removeClass('graph1').addClass('graph2');
	}

	if($('#point_register_form').length>0){
		$('#point_register_form').submit(validate_point_register);
	}
});

function notice_getCookie( name )
{
    var nameOfCookie = name + "=";
    var x = 0;
    while ( x <= document.cookie.length )
    {
        var y = (x+nameOfCookie.length);
        if ( document.cookie.substring( x, y ) == nameOfCookie ) {
                if ( (endOfCookie=document.cookie.indexOf( ";", y )) == -1 )
                        endOfCookie = document.cookie.length;
                return unescape( document.cookie.substring( y, endOfCookie ) );
        }
        x = document.cookie.indexOf( " ", x ) + 1;
        if ( x == 0 )
			break;
    }

    return "";
}

$(window).load(function(){
	if ( notice_getCookie( "Notice" ) != "done" )
	{
        window.open('/popup/start','','width=535,height=550'); // 팝업윈도우의 경로와 크기를 설정 하세요
	}

	if($('#point_register_form').length>0){
		point_type_change(1);
	}

	if($('#coupon_register_form').length>0){
		var time_type = $(':radio[name="time_type"]:checked').val();
		if(time_type == 0){
			toggle(0);
		}else if(time_type == 1){
			toggle(1);
			var data = $('#week_data').val();
			var arrayList = data.split(",")   
			var week_list = $('input:checkbox[name="week"]');
			for(var i=0 ; i < arrayList.length ; i++){
				week_list[parseInt(arrayList[i])].checked = true;
			}
		}
	}
});




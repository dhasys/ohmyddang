$(document).ready(function(){
	{% if url == "coupon/register" %}
	if($('#coupon_register_form').length>0){
		$('#coupon_register_form').submit(get_discount_percent);
	}
	{% endif %}

});
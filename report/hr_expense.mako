##coding=utf-8
%for exp in objects:
<table style='border-collapse : collapse;border : none;'>
    <tr><td colspan='4' style="text-align : center;border : none;"><h4>${user.company_id.name}</h4></td>
    <tr><td colspan='4' style="text-align : center;border : none;"><h3>报销凭证</h3></td></tr>
    <tr>
    <td style="width : 35mm;border : none;">单位:</td>
    <td style="width : 95mm;border : none;">${exp.department_id.name or ''|entity}</td>
    <td style="width : 20mm;border : none;">&nbsp;</td>
    <td style="width : 50mm;border : none;">${formatLang(exp.date,date = True) or ''|entity}</td>
    </tr>
</table>

<table style='border-collapse : collapse;border : 1px solid #000;'>
  <thead>
    <tr>
    <th style='border : thin solid gray;width : 35mm;'>日期</th>
    <th style='border : thin solid gray;width : 95mm;'>报销内容</th>
    <th style='border : thin solid gray;width : 20mm;'>金额</th>
    <th style='border : thin solid gray;width : 50mm;'>备注</th>
    </tr>
  </thead>
  <tbody>
    %for line in exp.line_ids:
      <tr>
        <td style='border : thin solid gray;'>${line.date_value}</td>
        <td style='border : thin solid gray;'>${line.name}/${line.unit_amount}/${line.unit_quantity}</td>
        <td style='border : thin solid gray;'>${line.total_amount}</td>
        <td style='border : thin solid gray;'></td>
      </tr>
    %endfor
  </tbody>
  <tfoot>
    <tr>
      <td colspan="3" style='border : thin solid gray;'>
        总计人民币&nbsp;&nbsp;
        ${to_big_rmb(exp.amount)}
      </td>
      <td style='border : thin solid gray;'>&yen;:${exp.amount}</td>
    </tr>
  </tfoot>
</table>
<table style="border-collapse : collapse;border : none;">
    <tr>
      <td colspan="4" style="width : 190mm;border : none;">
      经 办 人: ${exp.user_id.name} &nbsp;&nbsp;
      店    长: ${exp.user_id.name} &nbsp;&nbsp;
      部门经理: ${exp.user_id.name} &nbsp;&nbsp;
      </td>
    </tr>

    <tr>
      <td colspan="4" style="border : none;">
      总 会 计: ${exp.user_id.name} &nbsp;&nbsp;
      现金出纳: ${exp.user_id.name} &nbsp;&nbsp;
      副总经理: ${exp.user_id.name} &nbsp;&nbsp;
      总 经 理: ${exp.user_id.name} &nbsp;&nbsp;
      </td>
    </tr>
</table>
%endfor

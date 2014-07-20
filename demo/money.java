/**
 * @author shell-von
 * @date 2012-12-3
 * @see 金额转化，数据待测试
 */
import javax.swing.*;
public class Convert{
	private String[] ChineseNum={"零","壹","贰","叁","肆","五","陆","柒","捌","玖"};
	private String[] Chinese={"","拾","佰","千","万"};
	//处理小数点后面的数字
	public String afterDot(String num){
		String ans="";
		//得到小数点第一个位置的数字a
		int a=Integer.parseInt(String.valueOf(num.charAt(0)));
		if(num.length()==1){
			//只含角的情况
			if(a!=0)
				ans=ChineseNum[a].concat("角");
		}
		else{
			//转为角分的情况,得到小数点后第二位b，这里可以看出。并不得以原始数据做更改不会进行四舍五入。0.999依然独坐9角9分。而不是一元。
			int b=Integer.parseInt(String.valueOf(num.charAt(1)));
			if(a==0&&b==0)
				//0角0分的情况,注意这里不是ans="",这是为了在后面处理0.00这种特殊情况
				ans="整";
			else if (a==0){
				//只含分的情况,没有考虑0.01的情况。因为这个函数无法得知小数点前面的东西。需要在后面parserInput中考虑。
				ans="零".concat(ChineseNum[b].concat("分"));
			}
			else if(b==0){
				//只含角的情况
				ans=ChineseNum[a].concat("角");
			}
			else{
				//角分的情况
				ans=ChineseNum[a].concat("角").concat(ChineseNum[b].concat("分"));
			}
		}
		return ans;
	}
	//处理小数点前面的数字
	public String beforeDot(String num){
		String ans="";
		int len=num.length();
		if(len<6){
			//99999.99元以下
			ans=paser5Num(num);
		}
		else{
			String preString=num.substring(0,num.length()-4);//万以前
			String lstString=num.substring(num.length()-4);//万位以下
			//如果preString大于4.说明数字转化大于了亿，继续划分,其实类似于递归。这里情况比较少，所以直接使用条件语句
			if(preString.length()>4){
				String tmp=preString;
				String tmp2=lstString;
				preString=tmp.substring(0,tmp.length()-4);//亿以前
				lstString=tmp.substring(tmp.length()-4);//亿位以下
				if(preString.endsWith("0")&&!lstString.startsWith("0")){
					//读出一个零来
					ans=paser5Num(preString).concat("亿零")+paser5Num(lstString);
				}
				else{
					ans=paser5Num(preString).concat("亿")+paser5Num(lstString);
				}
				//上面完成后得到ans==**万，继续判断在倒数4-8位的数字，如果全是0.不读出万。
				if(lstString.contains("0000")){
					//4-8位阶段全是0.不用读出：万。如10000,1000一亿零一千。10001,1000,1一亿零1万一千.
					ans=ans+paser5Num(tmp2);
				}
				else{
					ans=ans+"万"+paser5Num(tmp2);
				}
			}
			//没有上亿
			else{
				if(preString.endsWith("0")&&!lstString.startsWith("0")){
					//读出一个零来
					ans=paser5Num(preString).concat("万零")+paser5Num(lstString);
				}
				else{
					ans=paser5Num(preString).concat("万")+paser5Num(lstString);
				}
			}
		}
		return ans;
	}
	//获取用户输入
	public String[] getUsrInput(){
		String numString=JOptionPane.showInputDialog("Please enter the num");
		while(!isValid(numString)){
			System.out.println("输入不合法");
			numString=JOptionPane.showInputDialog("Please enter the num again");
		}
		String[] ans=numString.split("[.]");//使用正则表达式匹配分别获得小数点前后的数字，使用\\.一个意思
		System.out.println("你要转化的金额为"+numString);
		return ans;
	}
	public boolean isValid(String numString){
		return numString.matches("^\\d+[.]?\\d*$");//判断字符串的合法性.认为1.是合法的
	}
	public String parserInput(String[] input){
		if(input[0].length()>13){
			//默认只能处理9亿9千9佰9拾9.99的数字
			System.out.println("Too big that can not convert it\n程序退出");
			System.exit(0);
		}
		String dotBefor=beforeDot(input[0]);
		if(!dotBefor.equals(""))
			dotBefor=dotBefor.concat("元");
		String dotAfter="";
		if(input.length==2){
			//长度为2.说明小数。处理后面
			dotAfter=afterDot(input[1]);
			if(input[0].equals("0")&&dotAfter.startsWith("零"))
				//处理0.01的情况。0.1不满足此种情况
				dotAfter=dotAfter.substring(1);
		}
		else{
			//木有小数，补上一个整字
			dotBefor=dotBefor.concat("整");
		}
		String ans=dotBefor.concat(dotAfter);
		if(ans.equals("整"))//处理0的特殊情况
			ans="零元整";
		return ans;
	}
	//处理数字
	public String paser5Num(String num){
		String ans="";
		int len=num.length();
		for(int i=0;i<len;i++){
			int a=Integer.parseInt(String.valueOf(num.charAt(i)));
			if(a==0){
				if(!ans.endsWith("零"))
					//上次没读0。这次读入，因为不存在连续两次读出0的情况。
					ans+=ChineseNum[a];
			}
			else{
				ans+=(ChineseNum[a]+Chinese[len-i-1]);
			}
		}
		if(ans.endsWith("零")){
			//去掉多读的0,比如。10000,上述结果会读出一万零。当然。0元的情况也满足。我也直接去掉这个0.留在parserInput中继续做处理。显得有点累赘、实在不想更改了
			ans=ans.substring(0,ans.length()-1);
		}
		return ans;
	}
	public static  void main(String[] args){
		Convert t = new Convert();
		int m=10;//用于测试。默认10次
		while(m!=0){
			System.out.println("倒数第"+m+"次测试");
			String input[] = t.getUsrInput();
			System.out.println(t.parserInput(input));
			m--;
		}
	}
}
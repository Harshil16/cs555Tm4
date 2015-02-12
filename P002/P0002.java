package p02;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;

public class P0002 {
	HashMap<String, Integer> hm;
	public P0002()
	{
		hm=new HashMap<String, Integer>();
		hm.put("INDI",0); hm.put("NAME",1); hm.put("SEX",1); hm.put("BIRT",1);
		hm.put("DEAT",1); hm.put("FAMC",1); hm.put("FAMS",1); hm.put("FAM",0);
		hm.put("MARR",1); hm.put("HUSB",1); hm.put("WIFE",1); hm.put("CHIL",1);
		hm.put("DIV",1); hm.put("DATE",2); hm.put("TRLR",0); hm.put("NOTE",0);
	}
	public static void main(String[] args) throws IOException
	{
		P0002 p1 = new P0002();
		//specify your ged file below.
		String filename="sample.ged";
		//specify your output result filename below
		String output="CS555HW.txt";
		p1.dojob(filename, output);
	}
	public  void dojob(String f,String o) throws IOException
	{
		BufferedReader br=new BufferedReader(new FileReader(f));
		BufferedWriter bw=new BufferedWriter(new FileWriter(o));
		String info="";
		String parent="";
		String[] index=new String[3];
		while((info=br.readLine())!=null)
		{
			String line=info;
			String lelnumber=info.split(" ")[0];
			bw.write(line);bw.newLine();
			bw.write(lelnumber);bw.newLine();
			String tag= (info.split(" ")[1].charAt(0)=='@'&&info.split(" ")[1].charAt(info.split(" ")[1].length()-1)=='@')?info.split(" ")[2]:info.split(" ")[1];
			if(Integer.parseInt(lelnumber)>=0||Integer.parseInt(lelnumber)<=2)
				index[Integer.parseInt(lelnumber)]=tag;
			if(!lelnumber.equals("0"))
				parent=index[Integer.parseInt(lelnumber)-1];
			else
				parent="";
			if(ifvalid(Integer.parseInt(lelnumber), tag,parent )&&(Integer.parseInt(info.split(" ")[0])>=0)&&Integer.parseInt(info.split(" ")[0])<=2){
				bw.write(tag);bw.newLine();
			}
			else{
				bw.write("Invalid tag");bw.newLine();
			}

		}
		br.close();
		bw.close();
	}
	public  boolean ifvalid(int l,String str,String parent)
	{
		if(!hm.containsKey(str))
			return false;
		if(str.equals("NAME")||str.equals("SEX")||str.equals("BIRT")||str.equals("DEAT")||str.equals("FAMC")||str.equals("FAMS"))
			return hm.get(str)==l?parent.equals("INDI"):false;
		if(str.equals("MARR")||str.equals("HUSB")||str.equals("WIFE")||str.equals("CHIL")||str.equals("DIV"))
			return hm.get(str)==l?parent.equals("FAM"):false;
		if(str.equals("DATE"))
			return hm.get(str)==l?(parent.equals("BIRT")||parent.equals("DEAT")||parent.equals("DIV")||parent.equals("MARR")):false;
		else
			return hm.get(str)==l;
	}
}

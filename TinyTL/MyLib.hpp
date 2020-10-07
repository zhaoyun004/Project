
//去掉line开头的空白字符。
string Skip_Blank(string line) {
	int i;
  for (i=0; i<line.length(); i++) {
    if (line[i]!=' ' && line[i]!='\t')
      break;
  }
	if (i<line.length()-i)
		return line.substr(i, line.length()-i);
	else
		return "";
}

//得到一行文本的头一个单词。
string Get_First(string line) {
  string s = "";
  for (int i=0; i<line.length(); i++) {
    if (line[i] != ' ' && line[i] != '\t' && i < line.length())
      s += line[i];
    else
      break;
  }
  return s;
}

//判断某字符串是否正整数
bool Is_Int(string s) {
  for (auto i:s) {
    if (isdigit(i) == false)
      return false;
  }
  return true;
}
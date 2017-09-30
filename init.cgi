#!/usr/local/bin/perl

require './lib/jcode.pl';


#2009年度の8月にこのヒアドキュメントは記しております。
#cssで大幅に改ざんされているが、common/inc/style.cssにおいて1430～1870行目にdivタグのid指定
#におけるmargin,float諸々のフォントの位置指定などが確認できる模様。

#独自開発印刷プログラムのためのフォームボタン

$print = qq(<div style="float:right;"><form>
<input type="button" value="ページを印刷" onclick="window.print();" />
</form></div>);



#カテゴリ別ランキング・全文/用語検索・カテゴリー・索引の４タイプの
#結果表示ページの為の下部表示。
#2009/08/01勝手に作り変えられたヤツは下。
#<div id="pageBack">
#<ul>
#<li><a onclick="history.back()" href="javascript: void(10);" class="linkList">戻る</a></li>
#</ul>
#</div>


$pr_js = qq(<br><br><div style="float:right;"><form>
<input type="button" value="ページを印刷" onclick="window.print();" />
</form></div><a href="http://www.nikkan.co.jp/html/search_word/index2009.html">トップへ戻る</a>
<hr><br><br><br><br><br><br><br><br>);



#カテゴリ別ランキング・全文/用語検索・カテゴリー・索引の４タイプの
#結果表示ページの際の上部タイトル表示

#$hyodai = qq(<div class="hyodai">
#<span style="color: white;"><b style="font-size:20px">
#産業用語集「モノづくり新語」</b></span></div>);

#2009/8/1改訂されたもの。ほぼすべてのcssをidでやってしまっとる。
#↓
$hyodai = qq(<h2 id="genre">産業用語集「モノづくり新語」</h2>);


#カテゴリ別ランキング・全文/用語検索・カテゴリー・索引の４タイプの
#結果表示ページの為の下部表示前の点線ｈｒタグ

$hr = qq(<hr color="#00000f" style="border-bottom: dotted 1px #8b4;" size="1">);



#八月二十二日に追加。google公告のglobal変数宣言。用語解説ページ用。

$jsggl = qq(<br><br><br><br><br>
<div style="float:right;"><form>
<input type="button" value="ページを印刷" onclick="window.print();" />
</form></div><a href="http://www.nikkan.co.jp/html/search_word/index2009.html">トップへ戻る</a>
<hr><p><script type="text/javascript">
<!--
google_ad_client = "pub-6543277328740531";
//Mid336x280TopBlue
google_ad_slot = "2549385494";
google_ad_width = 336;
google_ad_height = 280;
//-->
</script><script type="text/javascript"
src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script></p>);



#メッセージログ用

@wdy_strG = ('日', '月', '火', '水', '木', '金', '土');
($secG, $minG, $hourG, $mdayG, $monG, $yearG, $wdayG) = localtime(time);
$dateG = sprintf("%4d年%02d月%02d日(%s) %02d:%02d",
	$yearG + 1900, ++$monG, $mdayG, $wdy_strG[$wdayG],
	$hourG, $minG);



# 表示ファイル(２０１０年現在、未使用の可能性あり)
$htmldir = '/data/web/public/html/search_word/index.htm';

# ０９年度夏改ざんされた表紙ページ。
$htmldir2009 = '/data/web/public/html/search_word/index2009.html';

#投稿画像、用語アクセスIP記録ファイルが放り込まれてるアドレス
$imgdtr = 'http://www.nikkan.co.jp/html/search_word/srch_img/';

#imageディレクトリ(アクセスカウントディレクトリとも併用)
#公開時は分化。logディレクトリはそれぞれの用語の投稿番号
#をファイル名とし、（アクセス数:IPアドレス:ジャンル振り番）
#で与えられている。

$imgdir = "/data/web/public/html/search_word/srch_img/";
$logdir = "/data/web/public/html/search_word/srch_log/";



#これはどこで使われてるか
$cgiurl = 'http://www.nikkan.co.jp/cgi-bin/search/';

#検索結果用divタグ(これもどこで使われてるか)
$div = qq(<div style="background-color:white;position:absolute;left:200px;top:0;z-index:20;">);

#管理つーる(削除ルーチンの削除結果表示にも現在適用)
$ctrl_div = qq(<div class="textfield" style="background-color:#cfcfcf;overflow:auto;height:280px;width:450px">);

#お報せ用
$flowchart = <<END;
$ctrl_div
[$dateG]<br><br><ul>
<li>用語ページにはてなブックマークとtweetボタンを加えました。[2011/06/22]<br>
</li>
<li>週間用語検索データ集計ファイルの置き場所は<br>
<B>public/html/search_word/srch_img</B><br>
です。</li>
<li><a href="http://www.nikkan.co.jp/html/search_word/index2009.html" target="_blank">
いろいろ変えました。[2010/07/01]<br>
</li>
<li><a href="http://www.nikkan.co.jp/html/search_word/index2009.html" target="_blank">
用語検索ページ改訂版を一般公開ページ</a>に移植しました。[2009/08/05]<br>
</li>
<li>カテゴリ別ランキング表示・総合ランキング表示・カテゴリー表示ページを創りました。</li>
<li>索引プログラム誤作動の修正をしておきました。（2008年08月25日）</li>
<li>全文検索機能を追加しました。</li>
<li>用語を投稿した時間を表示させる機能を追加しました。</li>
<li>検索用語表示機能を追加しました。</li>
<li>新着用語表示機能テスト成功しました。(一週間以内の新着)</li>
<li>投稿記事修正機能を追加しました。</li>
<li>
<a href="http://www.nikkan.co.jp/html/search_word/index.htm" target="_blank">
用語検索ページ試作版version0.30をprivateディレクトリ上に掲載中。</a><br>
(カテゴリ検索・ランキング表示プログラムは制作中です。)<br>
</li>
<li>記事投稿・索引検索・記事表示機能初期テスト成功しました。</li>
<li>記事投稿入力機能を追加しました。</li>
<li>カテゴリー内の投稿記事を閲覧・削除する機能を追加しました。</li>
</ul>
</div>
END

# bodyタグ
$body = qq(<body bgcolor="#ffffff" text="#000000" link="#0000ff" vlink="#0000ff">);

# 管理CGI【URLパス】（現段階ではtest2.cgi）
$admincgi = './test2.cgi';

#navi.cgiのこと
$script = 'untitled.cgi';

#総登録件数、新着などのdatファイル
$numfile2 = "./num.dat";

# データファイル【サーバパス】
$logfile = "./contents.dat";

#logディレクトリにあるnum.dat(→2008年12月一般公開中現在未使用)
$numfile = "./log/num.dat";

#　大分類の二次元配列のグローバル宣言(小分類は必要なし)
@class = ('ＩＴ','エレクトロニクス','機械','自動車・航空','環境・エコ','金融・商況','素材・エネルギー','建設・住宅','食品','医療',
'流通・商社人物','政治・経済','その他');

#用語投稿入室画面パスワード
$pass = "hogehoge";

#用語投稿入室画面管理者ID
$auther = "haarp";

#何件表示できるかの数
$admin_view = 40;

# 条件定義（必要なしかもしれない→2008年12月一般公開中現在未使用）
@cond = ('AND','OR');

# 表示件数の選択（必要なしかもしれない→2008年12月一般公開中現在未使用）
@view = (10,20,50);

#新着用語登録件数。
$max_newwords = 12;

# カウンタリセットのタイミング(RANK.PLは未だ創ってない)
# 0 : リセットしない
# 1 : 毎週1回 → 毎週日曜日にリセット
# 2 : 10日毎に1回 → 毎月10,20,30日にリセット
# 3 : 毎月1回 → 毎月1日にリセット
$reset = 0;

# カウンタリセットの方式→2008年12月一般公開中現在未使用
# 0 : opendir関数を使用
# 1 : データファイルと付け合わせ (opendirが使用できない環境用)
$reset_type = 0;

# カウンタリセット用データ【サーバパス】→2008年12月一般公開中現在未使用
$resfile = "reset.dat";

#検索結果ページ繰越の表示件数
$list_view = 20;

# html側あいうえお順成形用２次元配列
@aiueo = (
['あ','い','う','え','お'],
['か','き','く','け','こ'],
['さ','し','す','せ','そ'],
['た','ち','つ','て','と'],
['な','に','ぬ','ね','の'],
['は','ひ','ふ','へ','ほ'],
['ま','み','む','め','も'],
['や','ゆ','よ','nl','nl'],
['ら','り','る','れ','ろ'],
['わ','を','nl','nl','nl'],
['A','B','C','D','E'],
['F','G','H','I','J'],
['K','L','M','N','O'],
['P','Q','R','S','T'],
['U','V','W','X','Y'],
['Z','nl','nl','nl','sn'],
['0','1','2','3','4'],
['5','6','7','8','9']
);

#-------------------------------------------------
#  データ入力・修正の為のルーチン。
#-------------------------------------------------

sub myform {
	local($no,$cls1,$cls2,$sub,$url,$nam,$msg,$time,$host) = @_;

	$msg =~ s/<br>/\n/g;

	print <<EOM;
<table cellpadding="4" cellspacing="1">
<tr>
  <th class="l">用語名</th>
  <td class="r"><input type="text" name="name" size="30" value="$nam"></td>
</tr>
<tr>
  <th class="l">添付画像</th>
  <td class="r"><input type="file" name="url" size="50" value="$url"></td>
</tr>
<tr>
  <th class="l">カテゴリー</th>
  <td class="r">
<select name="cate" size="5">
EOM
	
my $j=0;

foreach $i (@class) {
	if($j == $cls1){
		print "<option value=\"$j\" selected>$i\n";
	}else{
		print "<option value=\"$j\">$i\n";
		}
	$j++;
	}

print <<EOM;
  </select></td>
</tr>
<tr>
  <th class="l">振り仮名</th>
  <td class="r"><input type="text" name="sub" size="50" value="$sub"></td>
</tr>
<tr>
  <th class="l">用語解説</td>
  <td class="r"><textarea name="comment" cols="40" rows="6" wrap="soft">$msg</textarea></td>
</tr>
EOM

}

#-------------------------------------------------
#  htmlのインデックスページを作り変えるルーチン
#-------------------------------------------------

sub make_html{
	my ($all,$newwords,$kakunin_out) = @_;

	my $year = $yearG + 1900;
	my $mon = ++$monG;

	#===============================================================================
	#総合ランキング配列作成プログラム
	#===============================================================================

	my(@sort,@rank);

	open(RANK,"contents.dat") || &error("Open Error");
	while (<RANK>) {
		my ($no,$cls1,$cls2,$sub,$url,$nam,$msg,$time,$host) = split(/<>/);

		# カウントデータ読み込み
		open(DB,"$logdir${no}_${year}_7.dat") || next;
		my($count) = <DB>;
		close(DB);

		#右辺のipアドレスは代入しない。
		my ($cnt,$ip,$bla) = split(/:/, $count);

		my $rank_cnt = $no[$no];

		next if (!$cnt);

		#無名ハッシュの配列を用いるカテゴリランキング試作。先頭の値をアクセス数にしている
		#事に注目。$noは用語投稿番号だからこれも大事なので付する。
		push(@rank,"$cnt\0$no\0$cls1\0$cls2\0$sub\0$url\0$nam\0$msg\0$time\0$host");
		push(@sort,$cnt);
	
		}
	close(RANK);

	@rank = @rank[sort {$sort[$b] <=> $sort[$a]} 0 .. $#sort];

	#===============================================================================

	#===============================================================================
	#新着用語を投稿が古い順番から新しい順番に並び替える。
	#===============================================================================
	my($balance,@suji,@nw_name);

	foreach $balance (@{$newwords}){
		my ($suji,$nw_name) = split(/<>/,$balance);
		push(@suji, $suji);

		#$nw_nameの配列格納は念のためにやっているが、必要は今は無い
		push(@nw_name, $nw_name);
	}

	@$newwords = @$newwords [sort { $suji[$a] <=> $suji[$b]} 0..@$newwords];
	#===============================================================================

	my ($flg, @data, $ln, $x, $y, $furiban, $number, $nwwrd, $ofrank, $nam0x);
	my $ii = 0;
	my($r,$r2,$cnt2);

	open(DAT,"+<$htmldir2009") || &error("Open Error1:top page側のinit.cgi");

	flock(DAT, 2);

	while(<DAT>){
		#if (/<!-- aiueo_begin -->/) {
		#	$flg = 1;

		#	push(@data,$_);
		#}

		#if (/<!-- aiueo_end -->/) {
		#	$flg = 0;
		#	for($y = 0 ; $y < 18 ; $y++) {
		#			$number = ($y*5)+$x;
		#			$furiban=($y*5)+($x+1);
		#
		#			if ($number % 5 == 0) { push(@data,"<tr>\n"); }
		#
					#無名二次元配列$aiueoを宣言して、五行N列のテーブル化	
					#をする。
		#			if ($aiueo[$y][$x] eq 'nl'){
		#				push(@data,"<td align=\"center\" colspan=\"2\"width=\"36\" height=\"20\">");
		#				push(@data,"</td>\n");
		#			}elsif ($aiueo[$y][$x] eq 'sn'){
		#				push(@data,"<td align=\"center\" colspan=\"2\"width=\"36\" height=\"20\">");
		#				push(@data,"<a href=\"$cgiurl$script?kaisetsu=$furiban\">");
		#				push(@data,"<b>記号</b></a></td>\n");
		#			}else{
		#				#<b style="font-size:16">
		#				push(@data,"<td align=\"center\" colspan=\"2\"width=\"36\" height=\"20\">");
		#				push(@data,"<a href=\"$cgiurl$script?kaisetsu=$furiban\">");
		#				push(@data,"<b>$aiueo[$y][$x]</b></a><br>");
		#				push(@data,"</td>\n");
		#			}

		#			if ($number % 5 == 4) { push(@data,"</tr>\n"); }
		#		}
		#	}
		#}

		if (/<!-- figure_begin -->/) {
			$flg = 1;

			push(@data,$_);
		}

		if (/<!-- figure_end -->/) {
			$flg = 0;

			#新着用語件数を１２件以内にする。
			while(@{$newwords} > $max_newwords) {
				#pop関数を使うと新着の一番古い用語から10番目までが残ってしまうので×。
				shift @{$newwords};
				}

			@{$newwords} = reverse @{$newwords};

			foreach $nwwrd (@{$newwords}){

				if($nwwrd eq ''){next;}

				my($nw_no,$nw_name,$hiduke) = split(/<>/,$nwwrd);
				my $nw_name0x = url_enc($nw_name);

				#divだとかidだとかでガチガチにcssでかえてくれちゃったヤツの為の変更版
				push(@data, "<li><a href=\"$cgiurl$script?jump=$nw_no&description=$nw_name0x\">");
				#push(@data, "<b><a href=\"$cgiurl$script?jump=$nw_no&description=$nw_name0x\">");

				$hiduke=~s/^([0-9][0-9])/$1-1/e;
				
				push(@data, "$nw_name</a>&nbsp;<span>$hiduke</span></li>\n");
				#push(@data, "$nw_name</a></b><font size=\"2\">$hiduke</font><br>\n");
				
			}

		}

		#if(/^<title>\n/){
		#	$flg = 1;

		#	push(@data,$_);
		#}

		#if(<!-- how_many -->){

		#	push(@data, "用語総登録件数<br><b style=\"font=size:20px\">$all件</b>\n");

		#}

		if (/<!-- ranking_begin -->/) {
			$flg = 1;

			push(@data,$_);
		}

		if (/<!-- ranking_end -->/) {
			$flg = 0;

			while(@rank > $max_newwords) {
				pop @rank;
				}

			foreach $ofrank(@rank){

				$ii++;
				my ($cout,$no,$cls1,$cls2,$sub,$url,$nam,$msg,$time,$host) = split(/\0/,$ofrank);
			
				#Ｒ２があることで重複カウントを同一ランクにすることができる。
				if ($cnt2 != $cout) { $r = $ii; } else { $r = $r2; }

				$nam0x = url_enc($nam);

				#<li><span>1位</span>
				#<a href="http://www.nikkan.co.jp/cgi-bin/search/untitled.cgi?jump=304&description=%c0%fe%cb%c4%c4%a5%b7%b8%bf%f4" target="_self">
				#<b>線膨張係数</b></a></li>
				#なんか勝手につくりかえられたヤツのコード。class指定うざすぎ。
				#<li><span>$r位</span>
				#<a href="$cgiurl$script?jump=$no&description=$nam0x" target="_self"><b>$nam</b></a></li>\n

				push(@data, "<li><span>$r位</span>");
				push(@data, "<a href=\"$cgiurl$script?jump=$no&description=$nam0x\" target=\"_self\"><b>$nam</b></a></li>\n");
				
				#push(@data, "<font size=\"2\">$r位</font>");
				#push(@data, "<a href=\"$cgiurl$script?jump=$no&description=$nam0x\" target=\"_self\"><b>$nam</b></a><br>\n");

				$r2 = $r;
				$cnt2 = $cout;

				}

		}

		next if ($flg);

		push(@data,$_);

	}

	seek(DAT, 0, 0);
	print DAT @data;
	truncate(DAT, tell(DAT));
	close(DAT);

	&header($flg);
	print <<EOM;
<h4>$flg</h4>
総登録件数：$all件<br><br>【投稿内容】
<HR>
$kakunin_out
<HR>
一週間以内に投稿された新着用語<Br>
EOM

foreach $nwwrd (@{$newwords}){
	my ($new_no,$new_yogo,$new_york) = split(/<>/,$nwwrd);
	$new_york=~s/^([0-9][0-9])/$1-1/e; 
	print "<font size=\"3\">$new_yogo</font><BR>【$new_york】<br>";
}
	print <<EOM;
<br>
<h2><a href="http://www.nikkan.co.jp/html/search_word/index2009.html">
更新確認はこちらから。</a></h2>
EOM


	print <<EOM;
<form action="$admincgi" method="post">
<input type="hidden" name="auther" value="$in{'auther'}">
<input type="hidden" name="password" value="$in{'password'}">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="class" value="$class">
<input type="submit" value="前の処理画面に戻る">
</form>
<form action="$admincgi" method="post">
<input type="submit" value="最初の画面に戻る">
</form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  エンコードで%を加えない処理のルーチン。
#-------------------------------------------------

sub url_enc16 {
	local($_) = @_;

	if(/(\w)/g){$1;}
	s/\n$|\r$//g;
	s/(\W)/unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}

#-------------------------------------------------
#  通常のエンコードルーチン。
#-------------------------------------------------

sub url_enc {
	local($_) = @_;


	s/(\W)/'%'.unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}

#-------------------------------------------------
#  return関数をつかってないので$hostと$addrは
#  そのままホスト名とアドレス名として使用可能。
#-------------------------------------------------

sub get_host {
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	if ($host eq "") { $host = $addr; }
}

#-------------------------------------------------
#  ｈｔｍｌのヘッダ情報
#-------------------------------------------------
sub header{

	if ($headflag) { return; }
	my $title = shift;
	print "Content-type: text/html; charset=EUC-JP\n\n";
	
	print <<EOM;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<META HTTP-EQUIV="Content-Style-Type" content="text/css">
<title>$title</title></head>
$body
EOM

	$headflag = 1;

}

#------------------------------------------------
#  エラー処理
#------------------------------------------------
sub error {
	my $msg = shift;

	&header("ERROR");
	print <<EOM;
<div align="center">
<table border="1" cellpadding="18" cellspacing="0" width="450">
<tr><td class="tbl" align="center">
<h3>ERROR !</h3>
<font color="#dd0000">$msg</font>
<p>
<form>
<input type="button" value="前画面に戻る" onclick="history.back()">
</form>
</td></tr></table>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  あいうえお順を一次式分解
#-------------------------------------------------
sub linear{
	my $linear = shift;
	$linear_y = ($linear-1) % 5;
	$linear_x = ($linear-($linear_y+1))/5;
}

#-------------------------------------------------
#  投稿日時を割り出しRETURNするプログラム
#-------------------------------------------------
sub tm_network{

	my $oknu = shift;
	my @wdy_str = ('日', '月', '火', '水', '木', '金', '土');
	my ($sec, $min, $hour, $mday, $mon, $year, $wday)
		= localtime($oknu);
	my $togawajun = sprintf("%4d年%02d月%02d日(%s) %02d:%02d",
		$year + 1900, ++$mon, $mday, $wdy_str[$wday],
		$hour, $min);

	my $ikarishinji = sprintf("%02d／%02d(%s)",
		 ++$mon, $mday, $wdy_str[$wday]);

	return ($togawajun,$ikarishinji);
}

#------------------------------------------------
#  フッタ & 著作権表記 (削除不可)
#------------------------------------------------
sub footer {
	print <<EOM;
</div>
<div class="dspOnly" id="footerArea">
 <div style="text-align:center;">
<div style="text-align:center;">
<script type="text/javascript"><!--
google_ad_client = "pub-6543277328740531";
//Foot728x15LinkBlue
google_ad_slot = "2687728583";
google_ad_width = 728;
google_ad_height = 15;
//--></script>
<script type="text/javascript"
src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
 </div>

 <div id="pagetopAnchor"><a href="#pagetop">ページの先頭にもどる</a></div>

  <ul>
	<li><a href="/cop/cop04000.html">企業行動憲章</a></li>
	<li><a href="/privacy/">プライバシーポリシー</a></li>
	<li><a href="/cop/cop05000.html">著作権について</a></li>
	<li><a href="/cop/cop06000.html">環境問題等の取り組みについて</a></li>
	<li><a href="/cop/">会社案内</a></li>
	<li><a href="/recruit/">採用情報</a></li>
	<li><a href="/adv/">広告掲載ガイド</a></li>
	<li><a href="/sitemap/">サイトマップ</a></li>
	<li class="lastList"><a href="/toiawase/">お問合せ</a></li>
  </ul>

 <div id="copyRight"><p>掲載記事の無断転載を禁じます。発行株式会社HOGEHOGE </p><p>Copyright 2008 THE NIKKAN KOGYO  SHIMBUN,LTD.</p></div>
</div>

</DIV>

</body>
</html>
EOM
	exit;
}

1;


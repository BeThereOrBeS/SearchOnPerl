#!/usr/local/bin/perl

#print "Content-type: text/html; charset=EUC-JP\n\n";

require './init.cgi';
require './lib/cgi-lib.pl';

&ReadParse;

if ($in{'mode'} eq "default_new") { &data_mente_new; }
elsif ($in{'mode'} eq "default_edit" && $in{'geek'} ne "") { &data_mente_edit; }
elsif ($in{'mode'} eq "default_dele" && $in{'geek'} ne "") { &data_mente_dele; }
elsif ($in{'mode'} eq "default_csv") { &data_mente_csv; }
#else ($mode eq "setting") { &setting; }
login_check();

#以下よりサブルーチン。


#-------------------------------------------------
#  ログイン()
#-------------------------------------------------
sub login_check {

	#print "Content-type: text/html; charset=EUC-JP\n\n";

	if ($in{'password'} eq "" && $in{'auther'} eq "") {
		&enter_page;
	} elsif ($in{'password'} ne $pass || $in{'auther'} ne $auther) {
		&message("認証できません");
	} else {
		&admin_menu;
	}
}

#-------------------------------------------------
#  処理選択画面
#-------------------------------------------------
sub admin_menu {

	#my $page = 0;
	#foreach ( keys(%in) ) {
	##	if (/^page:(\d+)$/) {
	#		$page = $1;
	#		last;
	#	}
	#}
	my($date_up,$date_up2);

	&header("管理画面２");
	print <<EOM;
<form action="$admincgi" method="post">
<input type="submit" value="最初の画面に戻る">
</form>

<hr>
<b style="font-size:20px">下の”分類”メニューでカテゴリを選択すると今までに入力された記事の<br>
一覧が下方に表示されます。各記事のチェックボックスにチェックを入れて<br>
修正・削除の処理を行ってください。尚、修正処理は一処理につき<br>
一記事のみ可能です。最新の用語を入力する場合は”用語解説を入力”に<br>
チェックを入れて”処理を開始する”ボタンを押して入力してください。</b>
<form action="$admincgi" method="post" name="myForm">
<input type="hidden" name="auther" value="$in{'auther'}">
<input type="hidden" name="password" value="$in{'password'}">
<input type="hidden" name="gunre" value="$gunre">
分類：
<select name="gunre">
EOM
#@CLASS、分類のforeach。
my $j=0;

	foreach $i (@class) {
		if($in{'gunre'} == $j){print "<option value=\"$j\" selected>$i\n";}
		else{print "<option value=\"$j\">$i\n";}
		$j++;
		}

	print <<EOM;
</select>
<input type="submit" value="カテゴリー内の記事を表示">
</form>

<blockquote>
<font size="3">処理を選択して下さい。</font>
<form action="$admincgi" method="post">
<input type="hidden" name="auther" value="$in{'auther'}">
<input type="hidden" name="password" value="$in{'password'}">
<input type="hidden" name="gunre" value="$gunre">
<table border="1" cellspacing="0" cellpadding="5" width="350">
<tr bgcolor="#00ccff">
  <th nowrap><font size="-1">選択</font></th>
  <td width="100%">&nbsp; <font size="-1"><b>処理内容</b></font></td>
</tr>
<tr>
  <th><input type="radio" name="mode" value="default_new"></th>
  <td>&nbsp; <font size="-1">用語解説を入力</font></td>
</tr>
<tr>
  <th><input type="radio" name="mode" value="default_edit"></th>
  <td>&nbsp; <font size="-1">用語解説を修正</font></td>
</tr>

<tr>
  <th><input type="radio" name="mode" value="default_dele"></th>
  <td>&nbsp; <font size="-1">用語解説を削除</font></td>
</tr>
<tr>
  <th><input type="radio" name="mode" value="default_csv"></th>
  <td>&nbsp; <font size="-1">CSVファイル作成(建設中)</font></td>
</tr>
</table>
<p>
<input type="submit" value="処理を開始する">
</blockquote>
EOM


	#$in{class}が存在した場合、つまりカテゴリを選択すると
	#このcheckboxタグは展開される。
	my $i = 0;
	open(IN,"contents.dat") || &error("Open Error: $logfile");
	while (<IN>) {

		#print qq(<font size="4">$gunre</font>) if($gunre);
		
		my ($no,$cls1,$cls2,$sub,$url,$nam,$msg,$time,$host) = split(/<>/);

		#$cls1が空の場合、プログラム側で値"0"としている。
		($date_up,$date_up2) = &tm_network($time);
		if($cls1 eq $gunre){
			print "<br>";
			print qq |<img src="$imgdtr$url" width="20px">\n| if ($url);
			print qq |<input type="checkbox" name="geek" value="$no">\n|;
			&linear($cls2);
			#print $cls2."がaiueo".$linear_x."の".$linear_y;
			print qq |<b>用語名：$nam</b> [$class[$cls1] &gt; $aiueo[$linear_x][$linear_y] ]|;
			print qq |<br><font size="2">$msg</font>|;
			print qq |<br>【$host】 - $date_up|;
			print qq |<br>投稿番号$noの記事です。<br>\n|;
		}

		$i++;

	}
	close(IN);

}

sub data_mente_csv{

my ($out,@fl_nm,$str,@download,$rnk_y,$rnk_m);
my ($i,$r,$r2,$cr_out,$count,$i4,$i5,$i6);
my (@maxes,$i3,$j4,$p,$date_up,$date_up2,$cnt2);
my ($no_need,$all_csv);
my ($nen,$tuki,$shu);
my $but = [];

if ($in{'job'} eq "make_csv"){
	
	#月間ジャンル別のカテゴリーランキングと
	#総合ランキングのcsvファイルを持ってくるルーチンです。
	#untitled.cgi上で制作した週刊検索語ファイルもここで展開します。
	#&header("結果画面");
	print "Content-type: application/octet-stream\n";

	if($in{'monthly_rank'}){
		($rnk_y,$rnk_m) = split (/:/,$in{'monthly_rank'});
		print "Content-Disposition: attachment; filename=${rnk_y}_${rnk_m}.csv\n\n";
		($no_need,$all_csv) = &category_file($rnk_y,$rnk_m,1);

	#=========================================================================
	#月間の、ジャンル毎のアクセス数別ランキングをｃｓｖ化することが目的
	#=========================================================================

		for($i3=0;$i3<@class;++$i3){
			$j4 = @{$caterank[$i3]};
			push (@maxes,$j4);	
			}

		#ジャンルのランキングでもっとも長いランキングがあるジャンルの値を最初にもってくる。
		@maxes = sort {$b<=>$a} @maxes;

		for($i4=0;$i4<@class;$i4++){

			$i = 0;
			$r = 0;
			$r2 = 0;

			if($i4==@class-1){$but[$i][$i4]="$class[$i4]\n";}
			else{$but[$i][$i4]="$class[$i4],";}

			foreach $cr_out (@{$caterank[$i4]}) {
		
				$i++;

				my ($rank_cnt,$no,$bla,$cls2,$nam,$time) = split(/\0/,$cr_out);
				($date_up,$date_up2) = &tm_network($time);	
					#Ｒ２があることで重複カウントを同一ランクにすることができる。
				if ($cnt2 != $rank_cnt) { $r = $i; } else { $r = $r2; }
			
				# 結果表示。
				if($i4==@class-1){
					$but[$i][$i4]="[$r位]_${nam}_<アクセス数：${rank_cnt}>_<投稿日時：${date_up}>\n";
				}else{
					$but[$i][$i4]="[$r位]_${nam}_<アクセス数：${rank_cnt}>_<投稿日時：${date_up}>,";
				}
				$r2 = $r;
				$cnt2 = $rank_cnt;
				$but[$i][$i4]=&jcode::sjis($but[$i][$i4]);
			}

			if($i<$maxes[0]){
				$p = $maxes[0]-$i;
				for(0..$p){
					if($i4==@class-1){
						$but[$i][$i4]=",\n";
					}else{
						$but[$i][$i4]=",";
					} 
					$i++;
					$but[$i][$i4]=&jcode::sjis($but[$i][$i4]);
				}
			}
		}

		binmode(STDOUT);
		for($i6=0;$i6<$maxes[0];$i6++){
			for($i5=0;$i5<@class;$i5++){
				print "$but[$i6][$i5]";
			}
		}
		exit;

	}elsif($in{'weekly_words'}){
		#my ($nen,$tuki,$shu) = split (/:/,$in{'weekly_words'});
		#if (-e "$imgdir${nen}_${tuki}_${shu}.csv"){
		#	binmode(STDOUT);
		#	open(IN,"$imgdir${nen}_${tuki}_${shu}.csv") || die;
		#	binmode(IN);
		#	print <IN>;
		#	close;
		#	exit;
	}

	}
	&header("CSV出力画面");
	print <<EOM;
<form action="$admincgi" method="post">
<input type="submit" value="最初の画面に戻る"></form>
<ul>
<li>ＣＳＶ出力画面です。<b><span style="color: blue;">割合完成してきていると思います。</span></b>。
</ul>
<form action="$admincgi" method="post">
<input type="hidden" name="auther" value="$in{'auther'}">
<input type="hidden" name="password" value="$in{'password'}">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="job" value="make_csv">
<table border="1">
<tr>
  <td align="center">ジャンル別月間アクセス数</td>
  <td align="center">週間の検索語一覧</td>
  <td align="center">月間時間帯アクセス数</td>
</tr>
<tr>
<td>
<select name="monthly_rank">
EOM

my $j=0;
my $i;

opendir(DIR, $logdir);
my @file = readdir(DIR);
closedir(DIR);

#月・年・週・ジャンル（連想配列）・
foreach $str (@file){
	if($str =~/^[0-9]{3}_(.*)\.dat/){
		next if(grep (/$1/,@fl_nm) > 0);
		unshift @fl_nm,$1;
	}
}

sort @fl_nm;

foreach $i (@fl_nm) {
	my ($mth,$dy) = split /_/,$i;
	print "<option value=\"$mth:$dy\">$mth年$dy月\n";
	$j++;
	}

	print <<EOM;
</select>
</td>
<td>
<select name="weekly_words">
EOM

my $j=0;
my ($yr,$mt,$wk);

undef $i;
undef $str;
undef @file;
undef @fl_nm;

opendir(DIR2, $imgdir);
@file = readdir(DIR2);
closedir(DIR2);

#月・年・週・ジャンル（連想配列）・
foreach $str (@file){
	if($str =~/^([0-9]{4})_(.*)_(.)\.csv/){
		unshift @fl_nm,"$1:$2:$3";
	}
}

foreach $i (@fl_nm) {
	($yr,$mt,$wk) = split(/:/,$i);
	print "<option value=\"$i\">$yr年$mt月$wk週\n";
	$j++;
	}

	print <<EOM;
</select>
</td>
<td>
</td>
</tr>
</table>
<input type="submit" value="CSV出力開始！">
</form>
</body>
</html>
EOM

	exit;
}

#-------------------------------------------------
#  用語削除ルーチン
#-------------------------------------------------
sub data_mente_dele {

	my($line,$new,@num,@data,@new,@del_info,$del_num);

	# データNo読み取り
	open(DAT2,"+<$numfile2") || &error("Open Error1: $numfile");
	flock(DAT2, 2);
	@num = <DAT2>;

	# 改行をカット
	$num[0] =~ s/\n//;
	$num[1] =~ s/\n//;

	# １行目分割
	my($num,$all) = split(/,/, $num[0]);
	@new = split(/,/, $num[1]);

	#最新の用語をピックアップするための追加プログラム
	my @saishin;
	my $new_count = 0;

	#最新用語登録時間。
	my $now = time;

	#html側に保存されている、各用語の「アクセス数：最新のアクセスしてきた端末番号：カテゴリー番号」
	#のdatファイルを削除するためのコード。

	#my ($bla1,$bla2,$bla3,$bla4,$now_mon,$now_year) = localtime($now);

	# マスタDB読み取り
	open(DB2,"+<contents.dat") || &error("Open Error2: $logfile");
	flock(DB2, 2);
	while(<DB2>) {
		my($no,$cls1,$cls2,$sub,$url,$nam,$msg,$time,$host) = split(/<>/);

		# 削除データをマッチング
		my($f,$del);
		foreach $del ( split(/\0/, $in{'geek'}) ) {
			
			undef $f;
			# データNo(新着情報)の削除
			my($m,@tmp);

			#新着の登録番号をFOREACH。
			foreach $new (@new) {
				#削除する番号が新着の登録のなかに入っていたら$mを
				#一回カウントする。
				if ($new == $del) { 
					$m++; 
					next;
				}
				push(@tmp,$new);
			}
			if ($m) { @new = @tmp; }

			# マスタDBの削除
			if ($no == $del) {
				$f = 1;
				push(@del_info,"【用語：".$nam."】投稿番号 =".$no);

				#/data/web/からのパスから、カウントファイルと画像ファイルを削除。
				unlink("$imgdir$url");
				#unlink("$imgdir$del.dat");
				unlink("$logdir$del.dat");

				last;
			}
		}
		if (!$f) {
			#60日以内に登録されたもの。
			if($now - $time < 60*24*3600){
				my $ajyanendayo = &tm_network($time);
				push @saishin,"$no<>$nam<>$ajyanendayo";
				$new_count++;
				}
			push(@data,$_);
		}
	}

	# マスタDB更新
	seek(DB2, 0, 0);
	print DB2 @data;
	truncate(DB2, tell(DB2));
	close(DB2);

	# データNo更新
	foreach (@new) {
		$line .= "$_,";
	}
	$all = @data;

	# 更新データ
	$num[0] = "$num,$all,\n";
	$num[1] = "$line\n";

	seek(DAT2, 0, 0);
	print DAT2 @num;
	truncate(DAT2, tell(DAT2));
	close(DAT2);

	my $del_msg = $ctrl_div;
	for($del_num = 0;$del_num < @del_info;$del_num++) {
		$del_msg .= "<h3>".$del_info[$del_num]."</h3>";
		}
	$del_msg .= "<h2>以上の記事を削除しました</h2></div>";
	#&message($del_msg);
	&make_html($all,\@saishin,$del_msg);
}

#-------------------------------------------------
#  用語・修正投稿ルーチン
#-------------------------------------------------
sub data_mente_edit {

	if ($in{'job'} eq "edit2"){

		my (@data,@cls1,@cls2,@saishin);

		#画像データファイル作成プログラム
		my ($ext,$tmp,$upfile);
		my ($sec, $min, $hour, $mday, $mon, $year, $wday)= localtime(time);
		
		if($in{'url'}){
			foreach $tmp (@in){
				if ($tmp =~ /(.*)Content-type:(.*)/i){
				
					if ($2 =~ /image\/jpeg/i) { $ext = '.jpg'; }
					elsif ($2 =~ /image\/pjpeg/i) { $ext = '.jpg'; }
					elsif ($2 =~ /image\/gif/i) { $ext = '.gif'; }
					elsif ($2 =~ /image\/png/i) { $ext = '.png'; }
					else { $ext = 'NO_EXIST'; }
				}
			}
			$upfile = $hour.$min.$sec.$ext;
			chmod (0777,$upfile);
			open (EOUT,">$imgdir$upfile");
			binmode (EOUT);
			print EOUT $in{'url'};
			close (EOUT);
		}


		#最新用語登録時間。
		#$now = $time;

		#修正データの投稿時間を反映しない新着データ
		my $new_count = 0;

		open(EDIT,"+< $logfile") || &error("Open Error: $logfile");
		flock(EDIT, 2);
		while(<EDIT>) {
			my ($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$hos) = split(/<>/);

			if ($in{'geek'} == $no) {
				$cls1 = $in{'cate'};
				my $sub16=&url_enc($in{'sub'});

				#振り仮名クエリから先頭一文字を取り出すプログラム	
				if($sub16 =~/^%([0-9a-fA-F][0-9a-fA-F])%([0-9a-fA-F][0-9a-fA-F])/){
					$sub16 = lc($1.$2);
				}elsif($sub16 =~/^([A-Z0-9])/){
					$sub16 = $1;
				}

				my ($map, $name, $ln, $i);
				my ($x, $y);
		
				# 五十音、記号、アルファベット５文字×ｎ列のdatファイル。
				# リファレンス処理でなくinit.cgi冒頭記述の二次元配列を使用
				# するほうが間違いはないか。
				open(FILE, "<aiueo.dat")or die;
				flock(FILE, 2);
				while($ln = <FILE>) {
					chop $ln;
					push @{$map}, [split(/,/, $ln)];
				}
				close(FILE);
		
				#$cls2[0]にあいうえお・アルファベット順振り分け。
				#最後の80は「記号」カテゴリに該当する。
				for($y = 0 ; $y < 18 ; ++$y) {
					for($x = 0 ; $x < 5 ; ++$x) {
						my $map16 = &url_enc16($map->[$y][$x]);
						if($map16=~/^$sub16/){
							$cls2=($y*5)+($x+1);
						}elsif($map16=~/[a-f0-9]{4}$sub16/){
							$cls2=($y*5)+($x+1);
						}elsif($map16=~/[a-f0-9]{8}$sub16/){
							$cls2[0]=($y*5)+($x+1);
						}else{$cls2[0]=80;}
					}
				}

				$in{'comment'}=~s/\n/<br>/g;
				$in{'comment'}=~s/\r/<br>/g;

				#投稿時間をtime関数から引っ張ってくるのではなく、当時の投稿時間$timでpushする。
				$_ = "$no<>$cls1<>$cls2<>$in{'sub'}<>$upfile<>$in{'name'}<>$in{'comment'}<>$tim<>$host<>\n";
			}

			#60日以内に登録されたものを配列saishinにプッシュ。
			if($now - $tim < 60*24*3600){
				my $ajyanendayo = &tm_network($tim);
				push @saishin,"$no<>$nam<>$ajyanendayo";
				$new_count++;
			}

			push(@data,$_);
			push(@cls1,$cls1);
			push(@cls2,$cls2);
		}

		# 三段ソート
		@data = @data[sort { $cls1[$a] <=> $cls1[$b] || $cls2[$a] <=> $cls2[$b] } 0..$#cls1];

		# 更新
		seek(EDIT, 0, 0);
		print EDIT @data;
		truncate(EDIT, tell(EDIT));
		close(EDIT);

		#
		my $upsrc;

		if($upfile eq""){
			$upsrc="画像なし";
		}else{
			#$upsrc = qq(<img src="http://www.hogehoge.co.jp/html/private/search_test/$upfile" width="120">);
			$upsrc = qq(<img src="http://www.hogehoge.co.jp/html/search_word/srch_img/$upfile" width="120">);
		}


		#投稿確認画面出力ブログラム
		#修正投稿した時間と端末、time関数から日本語表記へtm network

		my $time = time;
		&get_host;
	
		my ($mendoi,$mouiya) = &tm_network($time);
	
		&linear($cls2[0]);

		my $kakunin = qq(
		<table border="1">
		<tr><th>修正した投稿番号</th><td>$in{'geek'}</td></tr>
		<tr><th>カテゴリー</th><td>$class[$in{'cate'}]</td></tr>
		<tr><th>索引</th><td>$aiueo[$linear_x][$linear_y]</td></tr>
		<tr><th>用語名</th><td>$in{'name'}</td></tr>
		<tr><th>読み方</th><td>$in{'sub'}</td></tr>
		<tr><th>投稿内容</th><td>$in{'comment'}</td></tr>
		<tr><th>画像</th><td>$upsrc</td></tr>
		<tr><th>投稿した端末の<BR>IPアドレス</th><td>$host</td></tr>
		<tr><th>修正投稿時間</th><td>$mendoi</td></tr>
		</table>);



		# HTML更新
		my $all = @data;
		&make_html($all,\@saishin,$kakunin);
	}

	my($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$hos);

	if ($in{'geek'} =~/\0[0-9]+/) { &error("修正は1記事づつです。".$in{'geek'}); }

	#$logfile=contents.datのこと。
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while(<IN>) {
		($no,$cls1,$cls2,$sub,$url,$nam,$msg,$time,$host) = split(/<>/);
		last if ($in{'geek'} == $no);
	}
	close(IN);


	&header("用語修正入力画面");
	print <<EOM;
<form action="$admincgi" method="post">
<input type="submit" value="最初の画面に戻る"></form>
<ul>
<li>修正画面です。
<li>振り仮名は日本語の場合平仮名、英語の場合最初の一文字を<br>
<b><span style="color: blue;">半角大文字</span></b>にしてください。
</ul>
<form action="$admincgi" method="post" enctype="multipart/form-data">
<input type="hidden" name="auther" value="$in{'auther'}">
<input type="hidden" name="password" value="$in{'password'}">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="job" value="edit2">
<input type="hidden" name="geek" value="$in{'geek'}">
EOM
	&myform($no,$cls1,$cls2,$sub,$url,$nam,$msg,$time,$host);

	print <<EOM;
</table>
<p>
<input type="submit" value=" 修正記事を投稿 ">
</form>
</body>
</html>
EOM
	exit;



}



#-------------------------------------------------
#  用語・新規投稿ルーチン
#-------------------------------------------------
sub data_mente_new {

if ($in{'job'} eq "new2"){
	my (@data,@cls1,@cls2);

	$cls1[0] = $in{'cate'};

	my $sub16=&url_enc($in{'sub'});

	#振り仮名クエリから先頭一文字を取り出すプログラム	
	if($sub16 =~/^%([0-9a-fA-F][0-9a-fA-F])%([0-9a-fA-F][0-9a-fA-F])/){
		$sub16 = lc($1.$2);
	}elsif($sub16 =~/^([A-Z0-9])/){
		$sub16 = $1;
	}

	my ($map, $name, $ln, $i);
	my ($x, $y);
		
	# 五十音、記号、アルファベット５文字×ｎ列のdatファイル。
	# あいうえおの濁音なども含まれている。これにより
	# 振り仮名クエリから自動的にあいうえお順に振り分けられている
	open(FILE, "<aiueo.dat")or die;
	flock(FILE, 2);
	while($ln = <FILE>) {
		chop $ln;
		push @{$map}, [split(/,/, $ln)];
	}
	close(FILE);
		
	#$cls2[0]にあいうえお・アルファベット順振り分け
	for($y = 0 ; $y < 18 ; ++$y) {
		for($x = 0 ; $x < 5 ; ++$x) {
			my $map16 = &url_enc16($map->[$y][$x]);
			if($map16=~/^$sub16/){
				$cls2[0]=($y*5)+($x+1);
			}elsif($map16=~/[a-f0-9]{4}$sub16/){
				$cls2[0]=($y*5)+($x+1);
			}elsif($map16=~/[a-f0-9]{8}$sub16/){
				$cls2[0]=($y*5)+($x+1);
			}
		}
	}
	
	#画像データファイル作成プログラム
	my ($ext,$tmp,$upfile);
	my ($sec, $min, $hour, $mday, $mon, $year, $wday)= localtime(time);
	
	
	if($in{'url'}){
		foreach $tmp (@in){
			if ($tmp =~ /(.*)Content-type:(.*)/i){
			
				if ($2 =~ /image\/jpeg/i) { $ext = '.jpg'; }
				elsif ($2 =~ /image\/pjpeg/i) { $ext = '.jpg'; }
				elsif ($2 =~ /image\/gif/i) { $ext = '.gif'; }
				elsif ($2 =~ /image\/png/i) { $ext = '.png'; }
				else { $ext = 'NO_EXIST'; }
			}
		}
		$upfile = $hour.$min.$sec.$ext;
		chmod (0777,$upfile);
		open (OUT,">$imgdir$upfile");
		binmode (OUT);
		print OUT $in{'url'};
		close (OUT);
	}
	
	my $time = time;
	&get_host;

	#print(-e "$imgdir$numfile2");
	# データNo
	open(DAT,"+<$numfile2") || &message("Open Error1:html側");
	flock(DAT, 2);
	my @num = <DAT>;

	my ($num,$all) = split(/,/, $num[0]);

	#用語の投稿された回数。
	$num++;

	$in{'comment'}=~s/\n/<br>/g;
	$in{'comment'}=~s/\r/<br>/g;
	if($upfile eq""){$uprsc="画像なし";}
	
	#登録番号・カテゴリー番号・あいうえお順番号・ふりがな・画像ファイル・用語名・解説・登録時間・ホストの順。
	$data[0] = "$num<>$cls1[0]<>$cls2[0]<>$in{'sub'}<>$upfile<>$in{'name'}<>$in{'comment'}<>$time<>$host<>\n";

	#最新の用語をピックアップするための追加プログラム
	my @saishin;
	my $new_count = 0;

	#最新用語登録時間及び出力用処理。
	my $now = $time;
	my $now_s = &tm_network($now);
	push @saishin,"$num<>$in{'name'}<>$now_s";

	#一番新しく投稿された用語をpushし、一つカウントをとる
	$new_count++;

	open(DB,"+<contents.dat") || &message("Open Error2: $logfile");
	flock(DB, 2);
	while(<DB>) {
		my ($no,$cls1,$cls2,$sub,$url,$nam,$msg,$time,$host) = split(/<>/);
		
		#60days以内に登録されたもの。
		if($now - $time < 60*24*3600){
			my $ajyanendayo = &tm_network($time);
			push @saishin,"$no<>$nam<>$ajyanendayo";
			$new_count++;
		}

		push(@data,$_);
		push(@cls1,$cls1);
		push(@cls2,$cls2);

	}

	# ソート(推薦フラグを削除したもの)
	@data = @data[sort { $cls1[$a] <=> $cls1[$b] ||  $cls2[$a] <=> $cls2[$b] } 0..$#cls1];
	# 更新
	seek(DB, 0, 0);
	print DB @data;
	truncate(DB, tell(DB));
	close(DB);

	#登録件数の実数。
	my $all = @data;

	$num[1] =~ s/\n//;
	$i = 0;
	my $line2 = "$num,";
	foreach ( split(/,/, $num[1]) ) {
		$i++;
		$line2 .= "$_,";
		#$NEWwordsグローバルスコープ
		last if ($i >= $new_words);
	}

	#更新データ
	$num[0] = "$num,$all,\n";
	$num[1] = "$line2\n";


	seek(DAT, 0, 0);
	print DAT @num;
	truncate(DAT, tell(DAT));
	close(DAT);

	my $upsrc;

	if($upfile eq""){
		$upsrc="画像なし";
	}else{
		#$upsrc = qq(<img src="http://www.hogehoge.co.jp/html/private/search_test/$upfile" width="120">);
		$upsrc = qq(<img src="http://www.hogehoge.co.jp/html/search_word/srch_img/$upfile" width="120">);

	}

	#投稿確認画面出力ブログラム

	my ($mendoi,$mouiya) = &tm_network($time);

	&linear($cls2[0]);

	my $kakunin = qq(
	<table border="1">
	<tr><th>投稿番号</th><td>$num</td></tr>
	<tr><th>カテゴリー</th><td>$class[$cls1[0]]</td></tr>
	<tr><th>索引</th><td>$aiueo[$linear_x][$linear_y]</td></tr>
	<tr><th>用語名</th><td>$in{'name'}</td></tr>
	<tr><th>読み方</th><td>$in{'sub'}</td></tr>
	<tr><th>投稿内容</th><td>$in{'comment'}</td></tr>
	<tr><th>画像</th><td>$upsrc</td></tr>
	<tr><th>投稿した端末の<BR>IPアドレス</th><td>$host</td></tr>
	<tr><th>投稿時間</th><td>$mendoi</td></tr>
	<tr><th>一ヶ月以内の用語登録件数</th><td>$new_count件</td></tr>
	</table>);


	#総登録件数と共にMAKE HTMLする。
	&make_html($all,\@saishin,$kakunin);

	#万が一の場合messageルーチンに飛ばす。
	#&message("$kakunin");

}
	&header("新着用語入力画面");
	print <<EOM;
<form action="$admincgi" method="post">
<input type="submit" value="最初の画面に戻る"></form>
<ul>
<li>必要内容を全て入力してください（画像は必要に応じて）。
<li>振り仮名は日本語の場合平仮名、英語の場合最初の一文字を<br>
<b><span style="color: red;">半角大文字</span></b>にしてください。
</ul>
<form action="$admincgi" method="post" enctype="multipart/form-data">
<input type="hidden" name="auther" value="$in{'auther'}">
<input type="hidden" name="password" value="$in{'password'}">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="job" value="new2">
EOM



	&myform();


	print <<EOM;
</table>
<p>
<input type="submit" value=" 記事を投稿 ">
</form>
</body>
</html>
EOM
	exit;


}

#-------------------------------------------------
#  入室画面
#-------------------------------------------------
sub enter_page {
	
print "Content-type: text/html; charset=EUC-JP\n\n";
print <<END;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP">

<script LANGUAGE="JavaScript">
<!--
setTimeout('window.opener=null;window.close();', 240000); 
-->
</script>
</head>
<center>
<form action="$admincgi" method="post">
<table bgcolor="#00ccdd" border="0" cellpadding="1">
<tr bgcolor="#00ccff">
	<th align="right"><font size="-1">用語解説</font></th>
	<th align="left" hight="20"><font size="-1">管理画面ページ</font></th>
</tr>
<tr>
	<td width="60" align="right">ID</TD>
	<td colspan="6"><input type="text" name="auther" maxlength="10" size="22" value=""></td>
</tr>
<TR>
	<TD width="60" align="right">Password</TD>
	<td colspan="6"><input type="password" name="password" maxlength="24" size="22" value=""></td>
</TR>
<TR>
	<TD colspan="4" align="center" height="30">
	 <input type="submit" value=" 用語入力画面へ ">&nbsp;&nbsp;&nbsp;
	</TD>
</TR>
</table>
</form>
</center>
$flowchart
<script language="javascript">
<!--
self.document.forms[0].auther.focus();
//-->
</script>
</body>
</html>
END

}

#-------------------------------------------------
#  完了メッセージ
#-------------------------------------------------
sub message {
	my $msg = shift;

	my $class = $in{'cate'};

	&header($msg);
	print <<EOM;
<h4>$msg</h4>
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
#  ｃｓｖの中身をつくるルーチン
#-------------------------------------------------

sub category_file{

	my $caterank=[];
	my $catesort=[];
	my $gunre_rank;
	my (@sort,@rank);

	my $uuu = 0;

	#my $flag = shift;
	my ($r_y,$r_m,$flag) = @_;

	#my $now = time;
	#my ($sec, $min, $hour, $mday, $mon, $year, $wday) = localtime($now);

	#$year += 1900;
	#$mon++;

	open(CR,"${imgdir}contents.dat") || &error("Open Error");
	while (<CR>) {
		my ($no,$cls1,$cls2,$sub,$url,$nam,$msg,$time,$host) = split(/<>/);

		# カウントデータ読み込み
		open(DB,"$logdir${no}_${r_y}_${r_m}.dat") || next;
		#open(DB,"$logdir${no}_${year}_${mon}.dat") || next;
		my($count) = <DB>;
		close(DB);

		#右辺のipアドレスは代入しない。
		my ($rank_cnt,$ip,$bla) = split(/:/, $count);

		next if (!$rank_cnt);

		#無名ハッシュの配列を用いるカテゴリランキング試作。先頭の値をアクセス数にしている
		#事に注目。$noは用語投稿番号だからこれも大事なので付する。
		push (@{ $caterank[$bla] },"$rank_cnt\0$no\0$bla\0$cls2\0$nam\0$time");
		push (@{ $catesort[$bla] },$rank_cnt);

		#print "<b>[".$caterank[$bla][0]."]</b><br>$uuu<hr>";

		push(@rank,"$rank_cnt\0$no\0$cls1\0$cls2\0$nam\0$time");
		push(@sort,$rank_cnt);

		$uuu++;

		}
	close(CR);

	my $m;

	for($m=0;$m<@class;$m++){
		@{$caterank[$m]} = @{$caterank[$m]}[sort {$catesort[$m][$b] <=> $catesort[$m][$a]} 0 .. @{$caterank[$m]}];
		$caterank[$m][0] =~tr/\0/,/;
		#print "$caterank[$m][0]<br>";
	}

	@rank = @rank[sort {$sort[$b] <=> $sort[$a]} 0 .. $#sort];
	
	

	#=======================================================
	#test2.cgi上data_mente_csvルーチン、
	#無名配列$caterankのアドレス渡し。。
	#=======================================================
	if($flag==1){
		return($caterank,\@rank);
		#exit;
	}

}


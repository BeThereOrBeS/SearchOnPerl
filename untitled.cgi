#!/usr/local/bin/perl

#serch側

print "Content-type: text/html; charset=EUC-JP\n\n";

require './init.cgi';
require './lib/cgi-lib.pl';

&ReadParse;

if ($in{'submit'}){
	&find;
}
elsif ($in{'all_submit'}){
	&all_find;
}
elsif ($in{'kaisetsu'}) {
 	&explain;
}
elsif (exists $in{'species'}) {
	&view;
}
elsif ($in{'jump'} && $in{'description'}) {
	require './lib/jump.pl';
	&jump;
}
elsif ($in{'cate_rank'} eq 'several') {
	&cr;
}
else{
	print "<h1>ERROR!</h1><br>「全文検索」ボタン、あるいは「用語検索」ボタンを押して検索実行してください。
		<br><br><a href=\"javascript:history.back()\">戻る</a>";
}

sub cr{
	my $caterank={};
	my $catesort={};
	my $gunre_rank;

	my $now = time;
	my ($sec, $min, $hour, $mday, $mon, $year, $wday) = localtime($now);

	$year += 1900;
	$mon++;

	open(CR,"contents.dat") || &error("Open Error");
	while (<CR>) {
		my ($no,$cls1,$cls2,$sub,$url,$nam,$msg,$time,$host) = split(/<>/);

		# カウントデータ読み込み
		open(DB,"$logdir${no}_${year}_${mon}.dat") || next;
		my($count) = <DB>;
		close(DB);

		#右辺のipアドレスは代入しない。
		my ($rank_cnt,$ip,$bla) = split(/:/, $count);

		next if (!$rank_cnt);

		#無名ハッシュの配列を用いるカテゴリランキング試作。先頭の値をアクセス数にしている
		#事に注目。$noは用語投稿番号だからこれも大事なので付する。
		push (@{$caterank[$cls1]},"$rank_cnt\0$no\0$cls1\0$cls2\0$sub\0$url\0$nam\0$msg\0$time\0$host");
		push (@{$catesort[$cls1]},$rank_cnt);
	
		}
	close(CR);

	my $m;

	for($m=0;$m<@class;$m++){
		@{$caterank[$m]} = @{$caterank[$m]}[sort {$catesort[$m][$b] <=> $catesort[$m][$a]} 0 .. @{$caterank[$m]}];
	}

	#カテゴリー別ランキングの為に用意した変数の数々。
	my($r,$i,$r2,$cnt2,$o,$cr_out,$sub0x);

	#===================================================================================================
	#============html側にあるindexのhtmlページをそっくりそのままcgiでsarvageするプログラム。============
	#===================================================================================================
	my ($kkn, @comfirm);

	open (EVERY,"$htmldir2009") or &error("htmlディレクトリopen失敗");
	@comfirm=<EVERY>;
	close (EVERY);

	#2009年8月改ざん版においては、common/css/style.cssでcatbox,catbigbox,catcenterなどの名称
	#でbackgrond url,width: 195px;,width: 130px;などなど、ランキング・用語名の幅指定をしている。
	#1850行目付近。なんでもかんでもcssにぶっこんでんじゃねぇよ。解読する身にもなってみろよ。

	for($kkn = 0;$kkn < @comfirm;$kkn++){
		if($comfirm[$kkn] =~/<!-- srch_begin -->/){

			print $hyodai;
			print "<table><tr>";

			for($o=0;$o<@class;$o++){

				if($o%5 == 0){print qq(<td valign="top" align="left" colspan="2" width="200px">);}

				$i = 0;
				$r = 0;
				$r2 = 0;
				print qq(<div style="height:320px;border:2px #E6E6FA solid;padding:5px;">);
				print qq(<h4><b><a href="$script?species=$o" target="_self">$class[$o]</a></b></h4>$hr<ul>);
				foreach $cr_out (@{$caterank[$o]}) {
	
					$i++;
					my ($count,$no,$cls1,$cls2,$sub,$url,$nam,$msg,$time,$host) = split(/\0/,$cr_out);
				
					#Ｒ２があることで重複カウントを同一ランクにすることができる。
					if ($cnt2 != $count) { $r = $i; } else { $r = $r2; }
			
					$sub0x = url_enc($sub);
					# 結果表示。及び[ $count ]はアクセス総数。
					print "<li><font size=\"2\">$r位<a class=\"linkList\" href=\"$script?jump=$no&description=$sub0x\"><b>$nam</b></a><br></font></li>\n";
	
					$r2 = $r;
					$cnt2 = $count;
	
					last if($r>5||$r2>5||$i>5);
				}
				print "</div>\n";

				if($o%5 == 4){print "</td>\n";}

			}

			print "</tr></table>";
			print $pr_js;
		}
		elsif($comfirm[$kkn] =~/<!-- title_rewrite -->/){
			print "<title>カテゴリ別ランキング - 産業用語集「モノづくり新語」";
			print " - 日刊オンボロ新聞 Business Line</title>\n";
		}
		elsif($comfirm[$kkn] =~/<!-- way_to_out -->/){
			my $wo2 = $kkn;
			until($comfirm[$wo2] =~/<!-- way_to_end -->/){
				$wo2++;
				}
			$kkn = $wo2;
		}
		elsif($comfirm[$kkn] =~/<!-- adding_phrase -->/){
			print qq(<li><a href="http://www.hogehoge.co.jp/html/search_word/index2009.html">産業用語集「モノづくり新語」</a></li>\n<li>用語</li>);
		}
		elsif($comfirm[$kkn] =~/<!-- way_out -->/){
			my $wo = $kkn;
			until($comfirm[$wo] =~/<!-- way_end -->/){
				$wo++;
				}
			$kkn = $wo;
		}
		else{
			print qq($comfirm[$kkn]);
		}
	}


}


sub find{

	my $k=0;
	my $i=0;
	my $allsrch;
	my (@find,@find_all,$cate_key);

	$in{'word'} =~ s/\xA1\xA1/ /g;
	my (@wd) =split(/\s+/, $in{'word'});

	if ($in{'cate'}){
		$cflag = 1;
		$cate_key = "$class[$in{'cate'}]";
	}

	# 入力内容を整理(euc対応)
	open(IN,"contents.dat") or die;
	while (<IN>) {
		local($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host) = split(/<>/);
		$allsrch=0;
		# カテゴリ検索
		#if ($cflag == 1) {
		#	if ($in{'cate'} != $cls1) { next; }
		#}
		my($flag,$wd);
		foreach $wd (@wd) {
			#index関数内では日本語でもバイト数として処理されるので数値変換の処理は不要
			if (index("$sub $nam", $wd) >= 0) {
				$flag = 1;
				$allsrch++;
			}
		}
	
		if ($flag) {
			$i++;
			#（フレーズのいずれかにマッチの場合）<IN>の生の情報が放り込まれる。
			push(@find,$_);
		}
	
		if($allsrch==@wd){
			$k++;
			#（フレーズ全てにマッチの場合）<IN>の生の情報が放り込まれる。
			push(@find_all,$_);
		}
	}
	close(IN);

	#===================================================
	#===================================================
	#$in{'word'}の情報をそのまま週刊検索ファイルに出力。
	word_csv();
	#===================================================
	#===================================================

	#===================================================================================================
	#============html側にあるindexのhtmlページをそっくりそのままcgiでsarvageするプログラム。============
	#===================================================================================================
	my ($kkn, @comfirm);
	my($r,$e,$d,$r2,$cnt2);

	open (RESULT,"$htmldir2009") or &error("htmlディレクトリopen失敗");
	@comfirm=<RESULT>;
	close (RESULT);

	for($kkn = 0;$kkn < @comfirm;$kkn++){
		if($comfirm[$kkn] =~/<!-- srch_begin -->/){

			print $hyodai;
	
			if ($i == 0 || $k == 0) {
				print "<b>検索した語【$in{'word'}】</b><br>用語が見つかりませんでした。$jsggl";
				#footer();
				#last;
			}elsif($in{'find_it'} eq "one" && $i >= 0){
				
				#検索した語数が一つ以上かそうでないか。
				if(@wd==1){
					print "<b>検索した語【$in{'word'}】を含む用語</b><br><b>$i</b>件見つかりました。$hr<br><ul>";
				}else{
					print "<b>検索した語【$in{'word'}】のいずれかの語を含む用語</b><br><br><b>$i</b>件見つかりました。$hr<br><ul>";
				}
		
				# ヒットした記事を展開
				$now = time;
				foreach (@find) {

					$e++;
					next if ($e < $page + 1);
					next if ($e > $page + $list_view);

					my($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host) = split(/<>/);
					# 結果を表示
					&mydata($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host);
				}

				my $from = $page + 1 ;
				my $to = $from + $list_view - 1;
				if ($to > $e) { $to = $e; }
			
				print qq(<br></ul>$hr&nbsp;( $e件中 $from - $to件を表\示 )<br><table><tr>);
				

				if ($page - $list_view >= 0 || $page + $list_view < $e) {

					my($x, $y, $start, $end);
					my $enwd = &url_enc($in{'word'});

					$start = 1;
					$end   = 25;

					print "<td>\n";

					$x = 1;
					$y = 0;
					while ($e > 0) {
				
						# 当ページ
						if ($page == $y) {
							print "| <b style=\"color:green\">$x</b>\n";
						# 切替ページ
						} elsif ($x >= $start && $x <= $end) {
							print "| <a href=\"$ENV{'SCRIPT_NAME'}?page=$y&find_it=one&submit=1&word=$enwd\">$x</a>\n";
						}

						$x++;
						$y += $list_view;
						$e -= $list_view;
					}

					print "|</td>\n";
				} else {
					print "<td></td>";
				}

				print qq(</tr></table>);

			}elsif($in{'find_it'} eq "all" && $k >= 0){
				print "<b>検索した語【$in{'word'}】全ての語を含む用語</b><br><b>$k</b>件見つかりました。$hr<br><ul>";
		
				# ヒットした記事を展開
				$now = time;
				foreach (@find_all) {

					$d++;
					next if ($d < $page + 1);
					next if ($d > $page + $list_view);

					my($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host) = split(/<>/);
					&mydata($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host);
				}

				my $from = $page + 1 ;
				my $to = $from + $list_view - 1;
				if ($to > $d) { $to = $d; }
			
				print qq(<br></ul>$hr&nbsp;( $d件中 $from - $to件を表\示 )<br><table><tr>);
				

				if ($page - $list_view >= 0 || $page + $list_view < $d) {

					my($x, $y, $start, $end);
					my $enwd = &url_enc($in{'word'});

					$start = 1;
					$end   = 25;

					print "<td>\n";

					$x = 1;
					$y = 0;
					while ($d > 0) {
				
						# 当ページ
						if ($page == $y) {
							print "| <b style=\"color:green\">$x</b>\n";
						# 切替ページ
						} elsif ($x >= $start && $x <= $end) {
							print "| <a href=\"$ENV{'SCRIPT_NAME'}?page=$y&find_it=all&submit=1&word=$enwd\">$x</a>\n";
						}

						$x++;
						$y += $list_view;
						$d -= $list_view;
					}

					print "|</td>\n";
				} else {
					print "<td></td>";
				}
				print qq(</tr></table>);
		
			}

		print $pr_js;

		}
		elsif($comfirm[$kkn] =~/<!-- adding_phrase -->/){
			print qq(<li><a href="http://www.hogehoge.co.jp/html/search_word/index2009.html">産業用語集「モノづくり新語」</a></li>\n<li>用語</li>);
		}
		#特定のページ内容を隠すプログラム
		elsif($comfirm[$kkn] =~/<!-- way_out -->/){
			my $wo = $kkn;
			until($comfirm[$wo] =~/<!-- way_end -->/){
				$wo++;
				}
			$kkn = $wo;
		}
		else{
			print $comfirm[$kkn];
		}
	}
	#===================================================================================================
	#===================================================================================================
	#===================================================================================================

}

sub all_find{

	my $k=0;
	my $i=0;
	my $allsrch;
	my (@find,@find_all,$cate_key);

	$in{'word'} =~ s/\xA1\xA1/ /g;
	my (@wd) =split(/\s+/, $in{'word'});

	if ($in{'cate'}){
		$cflag = 1;
		$cate_key = "$class[$in{'cate'}]";
	}

	# 入力内容を整理(euc対応)
	open(IN,"contents.dat") or die;
	while (<IN>) {
		local($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host) = split(/<>/);
		$allsrch=0;
		my($flag,$wd);
		foreach $wd (@wd) {
			#index関数内では日本語でもバイト数として処理されるので数値変換の処理は不要
			if (index("$sub $nam $msg", $wd) >= 0) {
				$flag = 1;
				$allsrch++;
			}
		}
	
		if ($flag) {
			$i++;
			#（フレーズのいずれかにマッチの場合）<IN>の生の情報が放り込まれる。
			push(@find,$_);
		}
	
		if($allsrch==@wd){
			$k++;
			#（フレーズ全てにマッチの場合）<IN>の生の情報が放り込まれる。
			push(@find_all,$_);
		}
	}
	close(IN);

	#===================================================
	#===================================================
	#$in{'word'}の情報をそのまま週刊検索ファイルに出力。
	word_csv();
	#===================================================
	#===================================================

	#===================================================================================================
	#============html側にあるindexのhtmlページをそっくりそのままcgiでsarvageするプログラム。============
	#===================================================================================================
	my ($kkn, @comfirm);
	my($r,$e,$d,$r2,$cnt2);

	open (RESULT,"$htmldir2009") or &error("htmlディレクトリopen失敗");
	@comfirm=<RESULT>;
	close (RESULT);

	for($kkn = 0;$kkn < @comfirm;$kkn++){
		if($comfirm[$kkn] =~/<!-- srch_begin -->/){

			print $hyodai;
	
			if ($i == 0 || $k == 0) {
				print "<b>検索した語【$in{'word'}】</b><br>記事が見つかりませんでした。$jsggl";
				#footer();
				#last;
			}elsif($in{'find_it'} eq "one" && $i >= 0){
				
				#検索した語数が一つ以上かそうでないか。
				if(@wd==1){
					print "<b>検索した語【$in{'word'}】を含む記事</b><br><b>$i</b>件見つかりました。$hr<br><ul>";
				}else{
					print "<b>検索した語【$in{'word'}】のいずれかの語を含む記事</b><br><b>$i</b>件見つかりました。$hr<br><ul>";
				}

				# ヒットした記事を展開
				$now = time;
				foreach (@find) {

					$e++;
					next if ($e < $page + 1);
					next if ($e > $page + $list_view);

					my($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host) = split(/<>/);
					# 結果を表示
					&mydata($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host);
				}

				my $from = $page + 1 ;
				my $to = $from + $list_view - 1;
				if ($to > $e) { $to = $e; }
			
				print qq(<br></ul>$hr&nbsp;( $e件中 $from - $to件を表\示 )<br><table><tr>);
				

				if ($page - $list_view >= 0 || $page + $list_view < $e) {

					my($x, $y, $start, $end);
					my $enwd = &url_enc($in{'word'});

					$start = 1;
					$end   = 25;

					print "<td>\n";

					$x = 1;
					$y = 0;
					while ($e > 0) {
				
						# 当ページ
						if ($page == $y) {
							print "| <b style=\"color:green\">$x</b>\n";
						# 切替ページ
						} elsif ($x >= $start && $x <= $end) {
							print "| <a href=\"$ENV{'SCRIPT_NAME'}?page=$y&find_it=one&all_submit=1&word=$enwd\">$x</a>\n";
						}

						$x++;
						$y += $list_view;
						$e -= $list_view;
					}

					print "|</td>\n";
				} else {
					print "<td></td>";
				}
				print qq(</tr></table>);
		
			}elsif($in{'find_it'} eq "all" && $k >= 0){
				print "<b>検索した語【$in{'word'}】全ての語を含む記事</b><br><b>$k</b>件見つかりました。$hr<br><ul>";
		
				# ヒットした記事を展開
				$now = time;
				foreach (@find_all) {

					$d++;
					next if ($d < $page + 1);
					next if ($d > $page + $list_view);

					my($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host) = split(/<>/);
					&mydata($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host);
				}

				my $from = $page + 1 ;
				my $to = $from + $list_view - 1;
				if ($to > $d) { $to = $d; }
			
				print qq(<br></ul>$hr&nbsp;( $d件中 $from - $to件を表\示 )<br><table><tr>);
				

				if ($page - $list_view >= 0 || $page + $list_view < $d) {

					my($x, $y, $start, $end);
					my $enwd = &url_enc($in{'word'});

					$start = 1;
					$end   = 25;

					print "<td>\n";

					$x = 1;
					$y = 0;
					while ($d > 0) {
				
						# 当ページ
						if ($page == $y) {
							print "| <b style=\"color:green\">$x</b>\n";
						# 切替ページ
						} elsif ($x >= $start && $x <= $end) {
							print "| <a href=\"$ENV{'SCRIPT_NAME'}?page=$y&find_it=all&all_submit=1&word=$enwd\">$x</a>\n";
						}

						$x++;
						$y += $list_view;
						$d -= $list_view;
					}

					print "|</td>\n";
				} else {
					print "<td></td>";
				}
				print qq(</tr></table>);
		
			}

		print $pr_js;
		if($i<20 || $k<20){for(0..30){print"<br>";}}

		}#<title>産業用語集「モノづくり新語」- 日刊オンボロ新聞 Business Line</title>
		elsif($comfirm[$kkn] =~/<!-- adding_phrase -->/){
			print qq(<li><a href="http://www.hogehoge.co.jp/html/search_word/index2009.html">産業用語集「モノづくり新語」</a></li>\n<li>用語</li>);
		}
		#特定のページ内容を隠すプログラム
		elsif($comfirm[$kkn] =~/<!-- way_out -->/){
			my $wo = $kkn;
			until($comfirm[$wo] =~/<!-- way_end -->/){
				$wo++;
				}
			$kkn = $wo;
		}
		else{
			print $comfirm[$kkn];
		}
	}


	#===================================================================================================
	#===================================================================================================
	#===================================================================================================


}


#------------------------------------------------
#  ■リスト表示
#------------------------------------------------
sub view {
	my($cate,$view_list,$now,$from,$to,@read);

	# ログ展開
	my $now = time;
	my $i = 0;

	my $species = $in{'species'};

	open(IN,"contents.dat") or die;
	while (<IN>) {
		my($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host) = split(/<>/);

		if ($cls1 =~/^$in{'species'}$/){
			$i++;
			push(@read,$_);
		}

	}
	close(IN);

	my ($kn, @comfir);
	my($r,$e,$r2,$cnt2);

	open (VIEW,"$htmldir2009") or print("htmlディレクトリopen失敗");
	@comfir=<VIEW>;
	close (VIEW);

	for($kn = 0;$kn < @comfir;$kn++){
		if($comfir[$kn] =~/<!-- gunre_begin -->/){

			print $hyodai;

			if ($i == 0) {
				print "<b>【$class[$in{'species'}]】</b>のカテゴリーに関する記事が見つかりませんでした。$jsggl";
				#footer();
				#last;
			}else{
				print "<b>【$class[$in{'species'}]】</b>のカテゴリーに関する記事<br><b>$i</b>件見つかりました。$hr<br><ul>";
				$now = time;
				foreach (@read) {

					$e++;
					next if ($e < $page + 1);
					next if ($e > $page + $list_view);

					my($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host) = split(/<>/);
					# 結果を表示
					&mydata($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host);
				}
			}

			my $from = $page + 1 ;
			my $to = $from + $list_view - 1;
			if ($to > $e) { $to = $e; }
			
			print qq(<br></ul>$hr&nbsp;( $e件中 $from - $to件を表\示 )<br><table><tr>);
				

			if ($page - $list_view >= 0 || $page + $list_view < $e) {

				my($x, $y, $start, $end);
				my $enwd = &url_enc($in{'word'});

				$start = 1;
				$end   = 25;

				print "<td>\n";

				$x = 1;
				$y = 0;
				while ($e > 0) {
				
					# 当ページ
					if ($page == $y) {
						print "| <b style=\"color:green\">$x</b>\n";
					# 切替ページ
					} elsif ($x >= $start && $x <= $end) {
						print "| <a href=\"$ENV{'SCRIPT_NAME'}?page=$y&species=$species\">$x</a>\n";
					}

					$x++;
					$y += $list_view;
					$e -= $list_view;
				}
				print "|</td>\n";
			} else {
				print "<td></td>";
			}
			print qq(</tr></table>);

			print $pr_js;

			if($i<20){for(0..30){print"<br>";}}

		}
		elsif($comfir[$kn] =~/<!-- title_rewrite -->/){
			print "<title>索引 - $class[$in{'species'}] - 産業用語集「モノづくり新語」";
			print " - 日刊オンボロ新聞 Business Line</title>\n";
		}
		elsif($comfir[$kn] =~/<!-- adding_phrase -->/){
			print qq(<li><a href="http://www.hogehoge.co.jp/html/search_word/index2009.html">産業用語集「モノづくり新語」</a></li>\n<li>用語</li>);
		}
		#特定のページ内容を隠すプログラム。
		elsif($comfir[$kn] =~/<!-- way_out -->/){
			my $w = $kn;
			until($comfir[$w] =~/<!-- way_end -->/){
				$w++;
				}
			$kn = $w;
		}
		else{
			print $comfir[$kn];
		}
	}	

}

sub explain{

	my $check;
	my $i = 0;
	my @contents;

	#索引のふり番を計算。
	&linear($in{'kaisetsu'});

	my $kaisetsu = $in{'kaisetsu'};

	if($aiueo[$linear_x][$linear_y] eq 'sn'){$aiueo[$linear_x][$linear_y]="記号";}

	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		my ($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$hos) = split(/<>/);

		if ($cls2=~/^$in{'kaisetsu'}$/){
			$i++;
			push(@contents,$_);
		}

		# ページ繰り越し（現在は創ってない）

	}
	close(IN);

	my ($kkn, @comfirm);
	my($r,$e,$d,$r2,$cnt2);

	open (EXPLAIN,"$htmldir2009") or &error("htmlディレクトリopen失敗");
	@comfirm=<EXPLAIN>;
	close (EXPLAIN);

	for($kkn = 0;$kkn < @comfirm;$kkn++){
		if($comfirm[$kkn] =~/<!-- srch_begin -->/){

			print $hyodai;

			if ($i == 0) {
				print "<b>【$aiueo[$linear_x][$linear_y]】</b>の項目に関する記事が見つかりませんでした。";
				#footer();
				#last;
			}else{
				print "<b>【$aiueo[$linear_x][$linear_y]】</b>の項目に関する記事<br><b>$i</b>件見つかりました。<br>$hr<br><ul>";
				$now = time;
				foreach (@contents) {

					$e++;
					next if ($e < $page + 1);
					next if ($e > $page + $list_view);

					my($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host) = split(/<>/);
					# 結果を表示
					&mydata($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host);
				}
			}

			my $from = $page + 1 ;
			my $to = $from + $list_view - 1;
			if ($to > $e) { $to = $e; }

			print qq(</ul><br>$hr&nbsp;( $e件中 $from - $to件を表\示 )<br><table><tr>);

			if ($page - $list_view >= 0 || $page + $list_view < $e) {

				my($x, $y, $start, $end);
				my $enwd = &url_enc($in{'word'});

				$start = 1;
				$end   = 25;

				print "<td>\n";

				$x = 1;
				$y = 0;
				while ($e > 0) {
					# 当ページ
					if ($page == $y) {
						print "| <b style=\"color:green\">$x</b>\n";
					# 切替ページ
					} elsif ($x >= $start && $x <= $end) {
						print "| <a href=\"$ENV{'SCRIPT_NAME'}?page=$y&kaisetsu=$kaisetsu\">$x</a>\n";
					}

					$x++;
					$y += $list_view;
					$e -= $list_view;
				}
				print "|</td>\n";
			} else {
				print "<td></td>";
			}
			print qq(</tr></table>);
			print $pr_js;
			if($e<20){for(0..30){print"<br>";}}
	
		}
		elsif($comfirm[$kkn] =~/<!-- title_rewrite -->/){
			print "<title>索引 - $aiueo[$linear_x][$linear_y] - 産業用語集「モノづくり新語」";
			print " - 日刊オンボロ新聞 Business Line</title>\n";
		}
		elsif($comfirm[$kkn] =~/<!-- adding_phrase -->/){
			print qq(<li><a href="http://www.hogehoge.co.jp/html/search_word/index2009.html">産業用語集「モノづくり新語」</a></li>\n<li>用語</li>);
		}
		#特定のページ内容を隠すプログラム。
		elsif($comfirm[$kkn] =~/<!-- way_out -->/){
			my $wo = $kkn;
			until($comfirm[$wo] =~/<!-- way_end -->/){
				$wo++;
				}
			$kkn = $wo;
		}
		else{
			print $comfirm[$kkn];
		}
	}	


}

sub mydata {

	#common/inc/style.cssの1494行目のrelatednewsとかいうidを参照のこと。imgファイルとか勝手に仕込まれてる。
	#仕様書くらい書いとけクソが

	my($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$host) = @_;
	my $sub0x = url_enc($sub);

	if (length($msg) > 90) {$msg = substr($msg,0,90) . '...';}

 	if($url){
		print "<li><a class=\"linkList\" href=\"$script?jump=$no&description=$sub0x\"><b>$nam</b></a>[画像あり]</li><br>$msg<br>";
	}else{
		#print qq(<div style="background: url(http://www.hogehoge.co.jp/html/search_word/common/images/com00174.gif) 0 bottom repeat-x;height:30px;">);
		print "<li><a class=\"linkList\" href=\"$script?jump=$no&description=$sub0x\"><b>$nam</b></a></li><br>$msg<br>";
		#print qq(<br></div>);
	}
}

sub word_csv{

	my ($sec, $min, $hour, $mday, $mon, $year, $wday)
		= localtime(time);

	my $date = sprintf("%02d:%02d", $hour, $min);

	my $w_v = $wday++;	
	$w_v = $mday - $w_v;
	$w_v = int($w_v/7) + 1;

	$year += 1900;
	$mon++;

	my $csv_name = "${year}_${mon}_${w_v}";

	$wday--;

	my(@csv,@d,@m,$dx,$cy,$dy,$buf,@buf2,$val,$guf,$guf2);


	unless (-e "$imgdir$csv_name.csv") {

		open(DAT,">$imgdir$csv_name.csv");

		$csv[1] = "sun,mon,tue,wed,thu,fri,sat\n";

		if($wday>0){
			$wday--;
			for(0..$wday){$guf.=","; $guf2.="0,";}
			$guf.="$in{'word'}_<$date>_$ENV{'REMOTE_ADDR'},";
			$guf2.="1,";
			$wday=$wday+2;
			for($wday..6){$guf.=","; $guf2.="0,";}
	
			$csv[0] = $guf2."\n";
			$csv[2] = $guf."\n";
		}else{
			$csv[0]	= "1,0,0,0,0,0,0\n";
			$csv[2] = "$in{'word'}_<$date>_$ENV{'REMOTE_ADDR'},,,,,,\n";
		}

		foreach $val(@csv){$val=&jcode::sjis($val);}

		seek(DAT, 0, 0);
		print DAT @csv;
		truncate(DAT, tell(DAT));
		close(DAT);

		chmod(0666, "$imgdir$csv_name.csv");


	}else{

		open(DAT2,"+<$imgdir$csv_name.csv");
		flock(DAT2, 2);
		
		@csv = <DAT2>;

		chomp $csv[0];
		@d = split /,/,$csv[0];

		$d[$wday]++;

		#最もアクセス数があった曜日のアクセス数を$m[0]にもってくる。
		@m = sort {$b<=>$a} @d;

		$csv[0] = join ",",@d;
		$csv[0].="\n";

		$d[$wday]=$d[$wday]+1;
		#if($dy==$d[$wday]){}

		for($dy=0;$dy<=$m[0];$dy++){

			$cy = 1+$dy;
			chomp $csv[$cy];
			@buf2 = split /,/,$csv[$cy];



			for($dx=0;$dx<7;$dx++){
				#当日のカウント数の升目$d[$wday]に合致する時、y軸上の正値となる
				if($dx==$wday&&$cy==$d[$wday]){
					$buf.="$in{'word'}_<$date>_$ENV{'REMOTE_ADDR'},";
				}elsif($dx==$wday&&$buf2[$dx] ne ""){
					$buf.="$buf2[$dx],";
				}elsif($dx!=$wday&&$buf2[$dx] ne ""){
					$buf.="$buf2[$dx],";
				}elsif($dx!=$wday&&$buf2[$dx] eq ""){
					$buf.=",";
				}
			}

			$buf.="\n";
			$csv[$cy] = $buf;

			undef $cy;
			undef $buf;
			undef @buf2;

		}

		foreach $val(@csv){$val=&jcode::sjis($val);}

		seek(DAT2, 0, 0);
		print DAT2 @csv;
		truncate(DAT2, tell(DAT2));
		close(DAT2);

	}

}



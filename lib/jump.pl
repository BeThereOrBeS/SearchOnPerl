

#------------------------------------------------
#  ■ジャンプ処理
#------------------------------------------------
sub jump {
	# IP取得
	my $addr = $ENV{'REMOTE_ADDR'};
	my ($no_b,$cls1_b,$cls2_b,$sub_b,$url_b,$nam_b,$msg_b,$tim_b,@wikied);

	# データオープン
	my ($flg,$no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim,$now,$bla);
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while(<IN>) {
		($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim) = split(/<>/);

		if ($in{'jump'} == $no) { 
			$flg = 1;
			($no_b,$cls1_b,$cls2_b,$sub_b,$url_b,$nam_b,$msg_b,$tim_b) =
			($no,$cls1,$cls2,$sub,$url,$nam,$msg,$tim);
			#last;
			}
		push (@wikied,"$no<>$nam");
	}
	close(IN);

	foreach $g (@wikied){

		my($wikisuji,$wikikoto) = split(/<>/,$g);

		#「require 'jcode.pl';」はinit.cgi上にあり、init.cgiをrequireしたuntitled.cgiを
		#経由してモジュールがここで使用できるようになっている。
		jcode::tr(\$wikikoto, '０-９Ａ-Ｚａ-ｚ', '0-9A-Za-z');
		jcode::tr(\$msg_b, '０-９Ａ-Ｚａ-ｚ', '0-9A-Za-z');

		#以下の５行でwikipediaのような用語リンクを自動アンカータグ生成する
		my $wikikoto16 = url_enc16($wikikoto);
		my $wk_t = length $wikikoto;
		my $position = index ($msg_b,$wikikoto);

		next if($position<0);
		substr($msg_b,$position,$wk_t,"<b><a href=untitled.cgi?jump=$wikisuji&description=$wikikoto16>$wikikoto</a></b>");
		#$msg_b =~s|($wikikoto)|<b><a href\=untitled\.cgi\?jump\=$wikisuji\&description\=$wikikoto16>$1<\/a><\/b>|o;
	}

	my $now = time;
	my ($sec, $min, $hour, $mday, $mon, $year, $wday) = localtime($now);

	#undef @buf2;
	#undef $f_cnt;

	$year += 1900;
	$mon++;

	if (!$flg) { &error("データが存在しません"); }

	#以降のプログラムにおいて、もうひとつcsvファイル制作プログラムをつくる。
	#その内容は「$ENV{HTTP_REFERER}によるリンク元ページ集計と時間別アクセス数」ファイル。
	#詳しくはITSOLUTIONのCSVプログラムを参考にする。

	# データなしのとき
	#unless (-e "$imgdir/$in{'jump'}.dat") {
	unless (-e "$logdir$in{'jump'}_${year}_${mon}.dat") {

		#open(DAT,"> $imgdir/$in{'jump'}.dat");
		open(DAT,">$logdir$in{'jump'}_${year}_${mon}.dat") or &error("logディレクトリ通常open失敗");;

		print DAT "1:$addr:$cls1_b";
		close(DAT);

		#chmod(0666, "$imgdir/$in{'jump'}.dat");
		chmod(0666, "$logdir$in{'jump'}_${year}_${mon}.dat");

	# データありのとき
	} else {

		# カウント
		#open(DAT,"+< $imgdir/$in{'jump'}.dat") or &error("htmlディレクトリopen失敗");
		open(DAT,"+<$logdir$in{'jump'}_${year}_${mon}.dat") or &error("$logdir$in{'jump'}.datのopen失敗");

		eval "flock(DAT, 2);";
		my $count = <DAT>;

		# データ分解
		my ($count,$ip,$bla) = split(/:/, $count);

		# カウントアップ(同一IPからのクリックを省く→「$ip ne $addr」)
		if ($ip ne $addr) {
			$count++;

			seek(DAT, 0, 0);
			print DAT "$count:$addr:$bla";
			truncate(DAT, tell(DAT));
		}
		close(DAT);
	}

	#====================================================================
	#==this is a stuff making csv of monthly axes count in every gunre===
	#====================================================================

#	my $csv_name = "gr_${year}_${mon}_${class[$cls1_b]}";

#	unless (-e "$logdir$csv_name.csv") {

#	} else {

#	}

	#====================================================================
	#==this is a stuff making csv of monthly axes count in every gunre===
	#====================================================================


	my ($kkn, @comfirm, $g);


	open (WORDS,"$htmldir2009") or &error("htmlディレクトリopen失敗");
	@comfirm=<WORDS>;
	close (WORDS);

	for($kkn = 0;$kkn < @comfirm;$kkn++){
		if($comfirm[$kkn] =~/<!-- result_begin -->/){

			&linear($cls2_b);

			print "$hyodai<h3 class=\"secondary\"><font size=\"5\">$nam_b</font></h3>
			<hr color=\"#ffffff\" size=\"0\">";
			#print "$hyodai<b><font size=\"4\">$nam_b</font></b><hr>";
			# 画像ありの場合
			if ($url_b) {
				print qq(<table>
					<tr><th>ジャンル:</th><td>$class[$cls1_b]</td></tr>
					<tr><th>読み方:</th><td>$sub_b</td></tr>
					</table>
					#<div id="bookmark">
					#<a href="http://twitter.com/share" class="twitter-share-button" data-count="none" data-via="hogehoge_BizLine">Tweet</a><script type="text/javascript" charset="utf-8" src="http://platform.twitter.com/widgets.js"></script>
					#</div>
					<hr color="#00000f" style="border-style:dashed" size="1">
					<div style="float:right;margin-left:10px;">
					<img src="$imgdtr$url_b" height="200" border="0" align="left" style="padding-right:15px;"><br>
					<center><b><font size=\"3\"><a href="$imgdtr$url_b" target="_blank">[拡大画像]</a></font></b></center></div>
					$msg_b);
			}else{
				print qq(<table border="0">
					<tr><th>ジャンル:</th><td>$class[$cls1_b]</td></tr>
					<tr><th>読み方:</th><td>$sub_b</td></tr>
					</table><div style="padding: 3px;">
					<a href="javascript:location.href='http://b.hatena.ne.jp/entry/'+encodeURI(document.location)"><img src="/common/images/b_entry.gif" width="16" height="12" style="border: none;"  /></a>
					<a href="http://twitter.com/share" class="twitter-share-button" data-count="none" data-via="hogehoge_BizLine">Tweet</a>
					<script type="text/javascript" charset="utf-8" src="http://platform.twitter.com/widgets.js">
					</script></div>
					$hr$msg_b);
			}
			print $jsggl;
			for(0..20){print"<br>";}
		}
		elsif($comfirm[$kkn] =~/<!-- specially made -->/){
			print " <b><font size=\"7\">$nam_b</font></b><hr>";
			# 画像ありの場合
			if ($url_b) {
				print qq(<table>
					<tr><th class="prnt">ジャンル:</th><td class="prnt">$class[$cls1_b]</td></tr>
					<tr><th class="prnt">読み方:</th><td class="prnt">$sub_b</td></tr>
					</table>
					<hr color="#00000f" style="border-style:dashed" size="1">
					<div style="float:right;margin-left:10px;">
					<img src="$imgdtr$url_b" height="350" border="0" align="left" style="padding-right:15px;"><br></div>
					<font size="5">$msg_b</font>);
			}else{
				print qq(<table border="0">
					<tr><th class="prnt">ジャンル:</th><td class="prnt">$class[$cls1_b]</td></tr>
					<tr><th class="prnt">読み方:</th><td class="prnt">$sub_b</td></tr>
					</table>
					<hr color="#00000f" style="border-style:dashed" size="1"><font size="5">$msg_b</font>);
			}
		}elsif($comfirm[$kkn] =~/<!-- title_rewrite -->/){
			print"<title>$nam_bとは 意味・解説 「モノづくり新語」日刊オンボロ新聞 Business Line</title>\n";
		}
		elsif($comfirm[$kkn] =~/<!-- adding_phrase -->/){
			print qq(<li><a href="http://www.hogehoge.co.jp/html/search_word/index2009.html">産業用語集「モノづくり新語」</a></li>\n<li> 用語</li>);
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

	exit;
}

sub linear{
	my $linear = shift;
	$linear_y = ($linear-1) % 5;
	$linear_x = ($linear-($linear_y+1))/5;
}

sub url_enc {
	local($_) = @_;

	s/(\W)/'%' .unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
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


1;


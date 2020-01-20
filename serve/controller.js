// Don't look, this is not pretty :)
;(function () {
  const $fen = $('#fen');
  const chess = {
    initialFen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    white: 'w',
    black: 'b',
    kings: new Set("Kk"),
    rooks: new Set("Rr"),
    pawns: new Set("Pp")
  };
  let prevFen = chess.initialFen;
  let stateList = [chess.initialFen];
  let perspective = 'w';
  let i = 0;

  function goTo(j) {
    if (j >= 0 && j <= stateList.length - 1) {
      i = j;
      $fen.val(stateList[j]);
      prevFen = stateList[j];
      board.position(stateList[j]);
    }
  }


  function newFen(fenish) {
    const prevTokens = prevFen.split(' ');
    const boardFen = fenish.split(' ');
    const out = new Array(prevTokens.length);

    for (let i = 0; i < prevTokens.length; i++) {
      const next = boardFen[i];
      out[i] = next !== undefined ? next : prevTokens[i];
    }
    const nextFen = out.join(' ');

    if (stateList[i] != nextFen) {
      $fen.val(nextFen);
      prevFen = nextFen;

      if (i != stateList.length - 1) {
        stateList = stateList.slice(0, i + 1);
      }
      stateList.push(nextFen);
      i++;
    }
  }

  function updatePlayMove(color, bFen, newCa) {
    const [, player, ca, , halfmove, move] = prevFen.split(' ');

    let oufFen = bFen;

    if (color == player) {
      $fen.addClass("playing")
      let nextPlayer = color == chess.white ? chess.black : chess.white;
      let moveInt = parseInt(move, 10);
      let nextMove = color == chess.black ? moveInt + 1 : moveInt;
      let ca_to = newCa ? newCa : ca;

      if (!ca_to) {
        ca_to = '-';
      }
      oufFen = [bFen, nextPlayer, ca_to, '-', parseInt(halfmove, 10) + 1, nextMove].join(' ');
    } else {
      $fen.removeClass("playing")
    }
    return oufFen;
  }

  const board = Chessboard('board', {
    draggable: true,
    onDrop(source, target, piece, newPos) {
      if (source != target) {
        newFen(updatePlayMove(piece[0], Chessboard.objToFen(newPos)));
      }
    },
    sparePieces: true,
    pieceTheme(piece) {
      return `/static/image/chess_${piece[0]}_${piece[1].toLowerCase()}.svg`
    }
  });

  function enhanceTheBoard() {
    const styles = "position:absolute;font-size:14px;color:black;";
    const topStyles = styles + "top:0;right:2px;";

    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].map((l, i) => {
      $('.square-' + l + '8').css("positions", "relative").append("<div style=\"" + topStyles + "\">" + i + "</div>")
    });

    const bottomStyles = styles + "bottom:2px;right:2px;";

    ['8', '7', '6', '5', '4', '3', '2', '1'].map((n, i) => {
      $('.square-h' + n).css("positions", "relative").append("<div style=\"" + bottomStyles + "\">" + i + "</div>")
    });
  }
  enhanceTheBoard();

  function reset() {
    i = 0;
    stateList = [chess.initialFen];
    board.start();
    $fen.val(chess.initialFen);
    $fen.addClass("playing");
  }
  reset();
  $('#reset').on('click', reset);

  $('#start').on('click', () => {
    board.start();
    $fen.addClass("playing");
    newFen(chess.initialFen);
  });

  $('#clear').on('click', () => {
    board.clear();
    newFen(board.fen());
  });

  $('#flip').on('click', () => {
    perspective = perspective == chess.white ? chess.black : chess.white;
    const $leftBtn = $('.castling > button')[0];
    $leftBtn.remove();
    $('.castling').append($leftBtn);
    board.flip();
    enhanceTheBoard();
  });

  $('#back').on('click', () => goTo(i - 1));
  $('#super-back').on('click', () => goTo(0));
  $('#forward').on('click', () => goTo(i + 1));
  $('#super-forward').on('click', () => goTo(Math.max(stateList.length - 1, 0)));

  function updateCastle() {
    function subtract(s1, s2) {
      const s = new Set(s2);
      let out = "";

      for (c of s1) {
        if (!s.has(c)) out += c;
      }
      return out;
    }
    const [, , ca] = prevFen.split(' ');
    const remove = perspective == chess.white ? "KQ" : "kq";
    const color = perspective == chess.white ? chess.white : chess.black;
    newFen(updatePlayMove(color, board.fen(), subtract(ca, remove)));
  }

  $('#castle-queen').on('click', () => {
    if (perspective == chess.white) {
      board.move('e1-c1', 'a1-d1');
    } else {
      board.move('e8-c8', 'a8-d8');
    }
    updateCastle();
  });

  $('#castle-king').on('click', () => {
    if (perspective == chess.white) {
      board.move('e1-g1', 'h1-f1');
    } else {
      board.move('e8-g8', 'h8-f8');
    }
    updateCastle();
  });

  function debounce(underlying, delay) {
    let timeoutId;
    let proxyThis;
    let proxyArgs;

    const action = () => {
      underlying.apply(proxyThis, proxyArgs);
      if (timeoutId) clearTimeout(timeoutId);
    };

    const proxy = function () {
      proxyThis = this;
      proxyArgs = arguments;

      if (timeoutId) clearTimeout(timeoutId);
      timeoutId = setTimeout(action, delay);
    };

    return [proxy, action];
  }

  [fenChangeProxy, fenChangeAction] = debounce(() => {
    const changed = $fen.val();
    const clean = changed.trim().replace(/[^-pPnNbBrRqQkKabcdefghw\/\s0-8]/g, '').replace(/\s+/g, ' ');
    const parsed = Chessboard.fenToObj(clean)

    if (parsed) {
      newFen(clean);
      $fen.addClass("playing");
      board.position(clean);
    } else {
      $fen.val(prevFen);
    }
  }, 1000);

  $fen.change(fenChangeProxy);
  $fen.blur(fenChangeAction);

  // ================ Engine Interop ================
  // Manual Get and choose to Play Move
  $getMove = $('#get-move');

  let suggestedNext;
  let cancel = false;

  function doMove(nextFen) {
    const parsed = Chessboard.fenToObj(nextFen)

    if (parsed) {
      newFen(nextFen);
      $fen.addClass("playing");
      board.position(nextFen);
    } else {
      $fen.val(prevFen);
    }
  }

  [applyMoveProxy, ] = debounce(() => {
    doMove(suggestedNext);
    suggestedNext = undefined;
  }, 500);

  async function getMove() {
    return axios
      .post('/api/analysis', {
        fen: $fen.val(),
        depth: parseInt($('#params').val() || 3, 10)
      })
      .then(resp => resp.data);
  }

  [getMoveProxy, ] = debounce(() => {
    getMove().then(({ move, fen }) => {
      if (cancel) return;

      suggestedNext = fen;
      if (move && move.length) {
        $getMove.text(move[0].slice(0, 6));
      }
    });
  });

  $getMove.on('click', () => {
    if (suggestedNext) {
      applyMoveProxy();
      $getMove.text("Get Move");
    } else {
      cancel = false;
      getMoveProxy();
    }
  });

  // Manual Get and Play Move
  $doMove = $('#do-move');

  [doMoveProxy, ] = debounce(() => {
    cancel = false;
    getMove().then(({ fen }) => doMove(fen));
  });
  $doMove.on('click', doMoveProxy);


  // Autoplay
  let keepPlaying = false;
  $play = $('#play');

  [playProxy, ] = debounce(function play() {
    keepPlaying && getMove().then(({ fen, done }) => {
      if (keepPlaying) {
        doMove(fen);

        if (done) {
          console.log("King Capture!");
          keepPlaying = false;
        }
        play();
      }
    });
  });
  const playText = 'Auto Play';
  const stopText = 'Stop';

  $play.on('click', () => {
    keepPlaying = !keepPlaying;
    $play.text($play.text() == playText ? stopText : playText);
    playProxy();
  });

  // Stop analysis for when it's running too long
  $stopAnalysis = $('#stop-analysis').on('click', () => {
    cancel = true;
    keepPlaying = false;
    $play.text(playText);
    return axios.delete('/api/analysis');
  });
})();

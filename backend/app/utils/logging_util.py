import logging
import os
import sys
from typing import Tuple, Dict, Any, Optional

if hasattr(sys, 'frozen'):
    _SRCFILE = 'logging%s__init__%s' % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _SRCFILE = __file__[:-4] + '.py'
else:
    _SRCFILE = __file__
_SRCFILE = os.path.normcase(_SRCFILE)


class LoggingUtil:
    """ Logging 유틸 클래스 """

    def __init__(self, name: str = 'fastapi') -> None:
        self.logger = logging.getLogger(name)

    def debug(self, msg: str, *args: Any, **kwargs: Dict[str, Any]) -> None:
        """ 기본 로거에 debug 호출을 위임합니다.

        Args:
            msg: 메세지
            *args: 추가 인자
            **kwargs: 키워드 인자
        """
        if self.logger.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, msg, args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Dict[str, Any]) -> None:
        """ 기본 로거에 info 호출을 위임합니다.

        Args:
            msg: 메세지
            *args: 추가 인자
            **kwargs: 키워드 인자
        """
        if self.logger.isEnabledFor(logging.INFO):
            self._log(logging.INFO, msg, args, **kwargs)

    def warn(self, msg: str, *args: Any, **kwargs: Dict[str, Any]) -> None:
        """ 기본 로거에 warn 호출을 위임합니다.

        Args:
            msg: 메세지
            *args: 추가 인자
            **kwargs: 키워드 인자
        """
        if self.logger.isEnabledFor(logging.WARN):
            self._log(logging.WARN, msg, args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Dict[str, Any]) -> None:
        """ 기본 로거에 error 호출을 위임합니다.

        Args:
            msg: 메세지
            *args: 추가 인자
            **kwargs: 키워드 인자
        """
        if self.logger.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, msg, args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Dict[str, Any]) -> None:
        """ 기본 로거에 critical 호출을 위임합니다.

        Args:
            msg: 메세지
            *args: 추가 인자
            **kwargs: 키워드 인자
        """
        if self.logger.isEnabledFor(logging.CRITICAL):
            self._log(logging.CRITICAL, msg, args, **kwargs)

    def _log(
            self,
            level: int,
            msg: str,
            args: Any,
            exc_info: Optional[bool] = None,
            extra: Optional[Dict[str, Any]] = None
    ) -> None:
        """ LogRecord를 생성 후 호출하는 Low-level logging이 loggers handlers 설정 기준으로 레코드 처리

        Args:
            level: 로그 레벨
            msg: 메시지
            args: 추가 인자
            exc_info: 예외 정보
            extra: 추가 정보
        """
        if _SRCFILE:
            try:
                file_name, line_num, func_name = self.find_caller()
            except ValueError:
                file_name, line_num, func_name = 'Unknown file', 0, 'Unknown function'
        else:
            file_name, line_num, func_name = 'Unknown file', 0, 'Unknown function'

        record = self.logger.makeRecord(self.logger.name,
                                        level,
                                        file_name,
                                        line_num,
                                        msg,
                                        args,
                                        exc_info,
                                        func_name, extra)
        self.logger.handle(record)

    @staticmethod
    def find_caller() -> Tuple[str, int, str]:
        """ 메서드 호출 위치를 가져옵니다.

        Returns:
            Tuple: 파일명, 라인 번호, 함수명
        """
        log_current_frame = logging.currentframe()

        if log_current_frame is not None:
            log_current_frame = log_current_frame.f_back

        results = '(unknown file)', 0, '(unknown function)'
        while hasattr(log_current_frame, 'f_code'):
            f_code = log_current_frame.f_code
            filename = os.path.normcase(f_code.co_filename)
            if filename == _SRCFILE:
                log_current_frame = log_current_frame.f_back
                continue
            results = (f_code.co_filename, log_current_frame.f_lineno, f_code.co_name)
            break

        return results

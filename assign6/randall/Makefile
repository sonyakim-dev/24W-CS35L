# Make x86-64 random byte generators.

# Copyright 2015, 2020, 2021 Paul Eggert

# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

# Optimization level.  Change this -O2 to -Og or -O0 or whatever.
OPTIMIZE =-Og

# The C compiler and its options.
CC = gcc
CFLAGS = $(OPTIMIZE) -g3 -Wall -Wextra -fanalyzer \
  -march=native -mtune=native -mrdrnd

# The archiver command, its options and filename extension.
TAR = tar
TARFLAGS = --gzip --transform 's,^,randall/,'
TAREXT = tgz

NUMBERS = 1 2 7 15 20 34 100
RAND_METHODS = rdrand lrand48_r /dev/urandom
OUT_METHODS = stdio 5 10

default: randall

randall: *.c *.h
	$(CC) $(CFLAGS) *.c -o $@

assignment: randall-assignment.$(TAREXT)
assignment-files = COPYING Makefile *.c *.h
randall-assignment.$(TAREXT): $(assignment-files)
	$(TAR) $(TARFLAGS) -cf $@ $(assignment-files)

submission-tarball: randall-submission.$(TAREXT)
submission-files = $(assignment-files) \
  notes.txt # More files should be listed here, as needed.
randall-submission.$(TAREXT): $(submission-files)
	$(TAR) $(TARFLAGS) -cf $@ $(submission-files)

repository-tarball:
	$(TAR) -czf randall-git.tgz .git

.PHONY: default clean assignment submission-tarball repository-tarball

clean:
	rm -f *.o *.$(TAREXT) randall

check: randall
	@$(foreach num,$(NUMBERS),\
		./$^ $(num) | wc -c | grep -q ^$(num)$$ && echo " >> SUCCESS: $(num)" ||\
		echo " >> FAIL: $(num)";)
	@$(foreach num,$(NUMBERS),\
		$(foreach opt,$(RAND_METHODS),\
			./$^ $(num) -i $(opt) | wc -c | grep -q ^$(num)$$\
			&& echo " >> SUCCESS: $(num) -i $(opt)"\
			|| echo " >> FAIL: $(num) -i $(opt)";))
	@$(foreach num,$(NUMBERS),\
		$(foreach opt,$(OUT_METHODS),\
			./$^ $(num) -o $(opt) | wc -c | grep -q ^$(num)$$\
			&& echo " >> SUCCESS: $(num) -o $(opt)"\
			|| echo " >> FAIL: $(num) -o $(opt)";))
	@$(foreach num,$(NUMBERS),\
		$(foreach in_opt,$(RAND_METHODS),\
			$(foreach out_opt,$(OUT_METHODS),\
				./$^ $(num) -i $(in_opt) -o $(out_opt)\
				| wc -c | grep -q ^$(num)$$\
				&& echo " >> SUCCESS: $(num) -i $(in_opt) -o $(out_opt)"\
				|| echo " >> FAIL: $(num) -i $(in_opt) -o $(out_opt)";)))

// Copyright 2017-2020 The Verible Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "common/util/type_traits.h"

#include "gmock/gmock.h"
#include "gtest/gtest.h"

namespace verible {
namespace {

TEST(MatchConst, NonConst) {
  static_assert(std::is_same<match_const<int, char>::type, int>::value);
  static_assert(std::is_same<match_const<const int, char>::type, int>::value);
}

TEST(MatchConst, Const) {
  static_assert(
      std::is_same<match_const<int, const char>::type, const int>::value);
  static_assert(
      std::is_same<match_const<const int, const char>::type, const int>::value);
}

}  // namespace
}  // namespace verible

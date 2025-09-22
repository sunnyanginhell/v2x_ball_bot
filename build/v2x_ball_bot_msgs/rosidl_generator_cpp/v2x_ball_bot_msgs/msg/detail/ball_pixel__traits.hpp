// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from v2x_ball_bot_msgs:msg/BallPixel.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_PIXEL__TRAITS_HPP_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_PIXEL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "v2x_ball_bot_msgs/msg/detail/ball_pixel__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace v2x_ball_bot_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const BallPixel & msg,
  std::ostream & out)
{
  out << "{";
  // member: u
  {
    out << "u: ";
    rosidl_generator_traits::value_to_yaml(msg.u, out);
    out << ", ";
  }

  // member: v
  {
    out << "v: ";
    rosidl_generator_traits::value_to_yaml(msg.v, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const BallPixel & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: u
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "u: ";
    rosidl_generator_traits::value_to_yaml(msg.u, out);
    out << "\n";
  }

  // member: v
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "v: ";
    rosidl_generator_traits::value_to_yaml(msg.v, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const BallPixel & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace v2x_ball_bot_msgs

namespace rosidl_generator_traits
{

[[deprecated("use v2x_ball_bot_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const v2x_ball_bot_msgs::msg::BallPixel & msg,
  std::ostream & out, size_t indentation = 0)
{
  v2x_ball_bot_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use v2x_ball_bot_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const v2x_ball_bot_msgs::msg::BallPixel & msg)
{
  return v2x_ball_bot_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<v2x_ball_bot_msgs::msg::BallPixel>()
{
  return "v2x_ball_bot_msgs::msg::BallPixel";
}

template<>
inline const char * name<v2x_ball_bot_msgs::msg::BallPixel>()
{
  return "v2x_ball_bot_msgs/msg/BallPixel";
}

template<>
struct has_fixed_size<v2x_ball_bot_msgs::msg::BallPixel>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<v2x_ball_bot_msgs::msg::BallPixel>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<v2x_ball_bot_msgs::msg::BallPixel>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_PIXEL__TRAITS_HPP_

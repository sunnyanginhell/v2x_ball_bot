// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from v2x_ball_bot_msgs:msg/BallPixel.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_PIXEL__BUILDER_HPP_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_PIXEL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "v2x_ball_bot_msgs/msg/detail/ball_pixel__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace v2x_ball_bot_msgs
{

namespace msg
{

namespace builder
{

class Init_BallPixel_v
{
public:
  explicit Init_BallPixel_v(::v2x_ball_bot_msgs::msg::BallPixel & msg)
  : msg_(msg)
  {}
  ::v2x_ball_bot_msgs::msg::BallPixel v(::v2x_ball_bot_msgs::msg::BallPixel::_v_type arg)
  {
    msg_.v = std::move(arg);
    return std::move(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::BallPixel msg_;
};

class Init_BallPixel_u
{
public:
  Init_BallPixel_u()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_BallPixel_v u(::v2x_ball_bot_msgs::msg::BallPixel::_u_type arg)
  {
    msg_.u = std::move(arg);
    return Init_BallPixel_v(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::BallPixel msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::v2x_ball_bot_msgs::msg::BallPixel>()
{
  return v2x_ball_bot_msgs::msg::builder::Init_BallPixel_u();
}

}  // namespace v2x_ball_bot_msgs

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_PIXEL__BUILDER_HPP_
